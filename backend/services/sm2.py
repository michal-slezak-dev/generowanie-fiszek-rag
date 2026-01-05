from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Tuple

class SpacedRepetitionAlgo(ABC):
    @abstractmethod
    def calculate(self, grade: int, repetitions: int, interval: int, easiness_factor: float) -> Tuple[int, int, float]:
        """
        Calculates the new study interval.
        args:
            grade (int): User rating (0-5).
            repetitions (int): Current number of successful repetitions.
            interval (int): Current interval - in days.
            easiness_factor (int): Current EF.
            
        returns:
            Tuple[int, int, float]: (new_interval, new_repetitions, new_easiness_factor)
        """
        pass

class SM2Algorithm(SpacedRepetitionAlgo):
    """
    Implementation of the (SM-2) algorithm.
    Source: https://www.supermemo.com/en/archives1990-2015/english/ol/sm2
    """
    
    def calculate(self, grade: int, repetitions: int, interval: int, easiness_factor: float) -> Tuple[int, int, float]:
        # 1. Update EF
        # EF' = EF + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))
        # q: grade (0-5)
        
        if grade < 3:
            # Correct response was not recalled. Start over again...
            new_repetitions = 0
            new_interval = 1
            new_easiness_factor = easiness_factor # EF doesn't change on failure in standard SM-2, or can decrease
            # We will follow the standard: EF changes happen, but repetitions reset.
        else:
            new_repetitions = repetitions + 1
            
        # EF update
        new_easiness_factor = easiness_factor + (0.1 - (5 - grade) * (0.08 + (5 - grade) * 0.02))
        
        if new_easiness_factor < 1.3:
            new_easiness_factor = 1.3
            
        # 2. Update interval
        if grade < 3:
            new_repetitions = 0
            new_interval = 1
        else:
            if new_repetitions == 1:
                new_interval = 1
            elif new_repetitions == 2:
                new_interval = 6
            else:
                new_interval = round(interval * new_easiness_factor)
                
        return new_interval, new_repetitions, float(round(new_easiness_factor, 2))
