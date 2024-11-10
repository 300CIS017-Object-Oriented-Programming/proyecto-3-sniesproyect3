class Lector:
    def __init__(self, filepath: str):
        self.filepath = filepath

    def read_excel(self) -> pd.DataFrame:
        try:
            data = pd.read_excel(self.filepath)
            return data
        except Exception as e:
            print(f"Error reading Excel file: {e}")
            return pd.DataFrame()
