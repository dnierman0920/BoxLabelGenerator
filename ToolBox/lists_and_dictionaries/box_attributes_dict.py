OZS_IN_A_LB = 16
LBS_IN_A_OZ = 1/16


class weight_conversion_helper:
    @staticmethod
    def convert_oz_to_lbs(units_in_oz: int):
        return units_in_oz*OZS_IN_A_LB

    @staticmethod
    def convert_weight_to_lbs(measuring_unit, units: int):
        return units if measuring_unit == "lbs" else weight_conversion_helper.convert_oz_to_lbs(units)


box = {
    "dimensions": {
        "measured_in": None,  # inches or cms
        "length": None,  # inches or cms -->
        "width": None,  # inches or cms
        "height": None  # inches or cms
    },
    "weight": {
        "measured_in": None,  # lbs or ounces
        "units": None  # lbs or ounces
    },
    "type": {
        "contains_mixed_skus": None,  # boolean
        "full_box": None,  # boolean
    },
    "qty_of_items": None,  # integer}
}
