class Car:
    def __init__(self, all_wheel, dealer_cost, horsepower, msrp, name):
        self.all_wheel = all_wheel
        self.dealer_cost = dealer_cost
        self.horsepower = horsepower
        self.msrp = msrp
        self.name = name
    
    @staticmethod
    def print_cars(cars: list[dict]):
        for car in cars:
            print(car)

    @staticmethod
    def from_dict(source):
        return Car(**source)

    def to_dict(self):
        return {
            "all_wheel": self.all_wheel,
            "dealer_cost": self.dealer_cost,
            "horsepower": self.horsepower,
            "msrp": self.msrp,
            "name": self.name
        }
    
    #TODO: make output string look nice 
    def __repr__(self):
        return f"{self.name}, msrp = {self.msrp}, horsepower = {self.horsepower}, dealer price = {self.dealer_cost}, all wheel = {self.all_wheel}"
