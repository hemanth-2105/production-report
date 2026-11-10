import pandas as pd

class file:
    def __init__(self,f_path,process_date = True):
        self.f_path = pd.read_excel(f_path)

        if process_date and "Date" in self.f_path.columns:
            self.f_path["Date"] = pd.to_datetime(
                self.f_path["Date"],
                errors="coerce"
            )

        numeric_col = ["Target Production","Production","Defects"]

        for col in numeric_col:
            if col in self.f_path.columns:
                self.f_path[col] = pd.to_numeric(self.f_path[col],errors="coerce")

    def head(self):
        return self.f_path.head()

    def column(self):
        return self.f_path.columns

    def shape(self):
        return self.f_path.shape

    def null_val(self):
        return self.f_path.isna().sum()

    def duplicated_val(self):
        return self.f_path.duplicated().sum()

    def drop_duplicates(self):
        return self.f_path.drop_duplicates()

class datas(file):
    def product_data(self):
        
        product = self.f_path.groupby(
            ["Product","Product Description"]
        ).agg(
            Target_production = ("Target Production","sum"),
            Production = ("Production","sum"),
            Defect = ("Defects","sum")
        ).reset_index()

        return product

    def department_data(self):
        department = self.f_path.groupby("Department").agg(
            Target_production = ("Target Production","sum"),
            Production = ("Production","sum"),
            Defect = ("Defects","sum")
        ).reset_index()

        return department

    def shift_data(self):
        shift = self.f_path.groupby("Shift").agg(
            Target_production = ("Target Production","sum"),
            Production = ("Production","sum"),
            Defect = ("Defects","sum")
        ).reset_index()

        return shift

    def daily_data(self):
        date = self.f_path.groupby("Date").agg(
            Target_production = ("Target Production","sum"),
            Production = ("Production","sum"),
            Defect = ("Defects","sum")
        ).reset_index()

        return date


# file1 = datas(r"C:\Users\Hemnath Raj\Downloads\manufacturing_production_data.xlsx")

# file2 = datas(r"C:\Users\Hemnath Raj\Downloads\product_names.xlsx",process_date=False)

