import time


class Chronos:
    def __init__(self):
        self.start_time = None
        self.end_time = None
        return

    def start(self):
        self.start_time = time.time()

    def end(self):
        if self.start_time is not None:
            self.end_time = time.time()
        else:
            raise Exception("Le chronomètre n'a pas été démarré.")
        return self.time()

    def time(self):
        if self.start_time is not None and self.end_time is not None:
            elapsed_time = self.end_time - self.start_time

            # Convertir le temps écoulé en heures, minutes et secondes
            hours = int(elapsed_time // 3600)
            minutes = int((elapsed_time % 3600) // 60)
            seconds = int(elapsed_time % 60)

            return f"Temps écoulé : {hours:02d}:{minutes:02d}:{seconds:02d}"
        else:
            raise Exception("Le chronomètre n'a pas été démarré et/ou arrêté.")