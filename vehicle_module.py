class Vehicle:
    def __init__(
        self,
        customer_name,
        phone,
        registration_no,
        model,
        vehicle_type="Normal"
    ):
        self.customer_name = customer_name
        self.phone = phone
        self.registration_no = registration_no
        self.model = model
        self.vehicle_type = vehicle_type
        self.service_charges = []

    def add_service(self, service_name, charge):
        self.service_charges.append((service_name, charge))

    def get_total_charge(self):
        return sum(charge for _, charge in self.service_charges)

    def __str__(self):
        return (
            f"Customer: {self.customer_name}\n"
            f"Phone: {self.phone}\n"
            f"Registration No: {self.registration_no}\n"
            f"Model: {self.model}\n"
            f"Vehicle Type: {self.vehicle_type}"
        )

    def __add__(self, other):
        if isinstance(other, Vehicle):
            return (
                self.get_total_charge()
                + other.get_total_charge()
            )

        return NotImplemented


class PremiumVehicle(Vehicle):
    def __init__(
        self,
        customer_name,
        phone,
        registration_no,
        model
    ):
        super().__init__(
            customer_name,
            phone,
            registration_no,
            model,
            "Premium"
        )