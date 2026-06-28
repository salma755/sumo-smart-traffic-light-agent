import numpy as np
import traci
from sumolib import checkBinary

# استيراد الثوابت الضرورية
from constants import (
    ACTION_TO_TL_PHASE,
    CELLS_PER_LANE_GROUP,
    INCOMING_EDGES,
    LANE_DISTANCE_TO_CELL,
    LANE_ID_TO_GROUP,
    ROAD_MAX_LENGTH,
    STATE_SIZE,
    TL_GREEN_TO_YELLOW,
    TRAFFIC_LIGHT_ID,
)
from generator import generate_routefile

class Environment:
    def __init__(self, n_cars_generated, max_steps, yellow_duration, green_duration, turn_chance, sumocfg_file, gui):
        self.n_cars_generated = n_cars_generated
        self.max_steps = max_steps
        self.yellow_duration = yellow_duration
        self.green_duration = green_duration
        self.turn_chance = turn_chance
        self.sumocfg_file = sumocfg_file 
        self.gui = gui
        self.step = 0

    def activate(self):
        """بدء محاكاة SUMO"""
        self.step = 0
        sumo_binary = checkBinary("sumo-gui" if self.gui else "sumo")
        sumo_cmd = [
            sumo_binary, "-c", self.sumocfg_file, 
            "--no-step-log", "true",
            "--waiting-time-memory", str(self.max_steps)
        ]
        traci.start(sumo_cmd)

    def deactivate(self):
        """إغلاق المحاكاة"""
        traci.close()

    def generate_routefile(self, seed):
        """توليد السيارات"""
        generate_routefile(seed, self.n_cars_generated, self.max_steps, self.turn_chance)

    def is_over(self):
        """التحقق من انتهاء الوقت"""
        return self.step >= self.max_steps

    def get_state(self):
        """رصد مواقع السيارات (نفس منطق الأصل بدقة)"""
        state = np.zeros(STATE_SIZE)
        for car_id in traci.vehicle.getIDList():
            lane_id = traci.vehicle.getLaneID(car_id)
            lane_group = LANE_ID_TO_GROUP.get(lane_id)
            
            if lane_group is not None:
                lane_pos = traci.vehicle.getLanePosition(car_id)
                # عكس الموقع (0 هو عند الإشارة)
                dist_from_tl = ROAD_MAX_LENGTH - lane_pos
                dist_from_tl = max(0.0, min(ROAD_MAX_LENGTH, dist_from_tl))
                
                # تحديد الخلية بناءً على المسافة
                lane_cell = 0
                for dist, cell in LANE_DISTANCE_TO_CELL.items():
                    if dist_from_tl <= dist:
                        lane_cell = cell
                        break
                
                # حساب الموقع في المصفوفة
                index = (lane_group * CELLS_PER_LANE_GROUP) + lane_cell
                if 0 <= index < STATE_SIZE:
                    state[index] = 1.0
        return state

    def get_cumulated_waiting_time(self):
        """حساب مجموع الانتظار (للمكافأة)"""
        wait_time = 0.0
        for car_id in traci.vehicle.getIDList():
            if traci.vehicle.getRoadID(car_id) in INCOMING_EDGES:
                wait_time += traci.vehicle.getAccumulatedWaitingTime(car_id)
        return wait_time

    def execute(self, action):
        """تنفيذ الأكشن مع الطور الأصفر (مطابق للأصل)"""
        target_phase = ACTION_TO_TL_PHASE[action]
        current_phase = traci.trafficlight.getPhase(TRAFFIC_LIGHT_ID)

        # 1. الانتقال للأصفر إذا تغير القرار
        if target_phase != current_phase:
            yellow_phase = TL_GREEN_TO_YELLOW[current_phase]
            traci.trafficlight.setPhase(TRAFFIC_LIGHT_ID, yellow_phase)
            self._simulate(self.yellow_duration)

        # 2. الانتقال للأخضر
        if not self.is_over():
            traci.trafficlight.setPhase(TRAFFIC_LIGHT_ID, target_phase)
            self._simulate(self.green_duration)

    def _simulate(self, duration):
        """تحريك الوقت في SUMO"""
        for _ in range(duration):
            if not self.is_over():
                traci.simulationStep()
                self.step += 1

    def get_queue_length(self):
        """حساب عدد السيارات المتوقفة"""
        total_queue = 0
        for edge in INCOMING_EDGES:
            total_queue += traci.edge.getLastStepHaltingNumber(edge)
        return int(total_queue)