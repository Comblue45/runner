class IDManager:
    current_id = 0

    @staticmethod
    def get_next_id() -> int:
        return_id = IDManager.current_id
        IDManager.current_id += 1
        return return_id