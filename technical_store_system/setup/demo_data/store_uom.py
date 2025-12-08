"""
Store UOM Demo Data
27 default Units of Measure for testing and initial setup
"""

DEMO_UOMS = [
	# Quantity-based (whole numbers)
	{"uom_name": "Each", "uom_symbol": "Ea", "uom_type": "Quantity", "must_be_whole_number": 1, "enabled": 1, "is_default": 1, "description": "Individual items, pieces, units"},
	{"uom_name": "Nos", "uom_symbol": "Nos", "uom_type": "Quantity", "must_be_whole_number": 1, "enabled": 1, "description": "Numbers (same as Each)"},
	{"uom_name": "Piece", "uom_symbol": "Pc", "uom_type": "Quantity", "must_be_whole_number": 1, "enabled": 1, "description": "Individual pieces"},
	{"uom_name": "Pair", "uom_symbol": "Pr", "uom_type": "Quantity", "must_be_whole_number": 1, "enabled": 1, "description": "Pair of items (2 pieces)"},
	{"uom_name": "Set", "uom_symbol": "Set", "uom_type": "Quantity", "must_be_whole_number": 1, "enabled": 1, "description": "Set of items"},
	{"uom_name": "Dozen", "uom_symbol": "Dz", "uom_type": "Quantity", "must_be_whole_number": 1, "enabled": 1, "description": "12 pieces"},
	{"uom_name": "Box", "uom_symbol": "Box", "uom_type": "Quantity", "must_be_whole_number": 1, "enabled": 1, "description": "Boxed items"},
	{"uom_name": "Pack", "uom_symbol": "Pk", "uom_type": "Quantity", "must_be_whole_number": 1, "enabled": 1, "description": "Package of items"},
	{"uom_name": "Bundle", "uom_symbol": "Bdl", "uom_type": "Quantity", "must_be_whole_number": 1, "enabled": 1, "description": "Bundle of items"},
	{"uom_name": "Carton", "uom_symbol": "Ctn", "uom_type": "Quantity", "must_be_whole_number": 1, "enabled": 1, "description": "Carton box"},
	
	# Weight
	{"uom_name": "Kilogram", "uom_symbol": "Kg", "uom_type": "Weight", "must_be_whole_number": 0, "enabled": 1, "description": "Weight in kilograms"},
	{"uom_name": "Gram", "uom_symbol": "g", "uom_type": "Weight", "must_be_whole_number": 0, "enabled": 1, "description": "Weight in grams"},
	{"uom_name": "Ton", "uom_symbol": "t", "uom_type": "Weight", "must_be_whole_number": 0, "enabled": 1, "description": "Weight in metric tons"},
	
	# Volume
	{"uom_name": "Liter", "uom_symbol": "L", "uom_type": "Volume", "must_be_whole_number": 0, "enabled": 1, "description": "Volume in liters"},
	{"uom_name": "Milliliter", "uom_symbol": "mL", "uom_type": "Volume", "must_be_whole_number": 0, "enabled": 1, "description": "Volume in milliliters"},
	{"uom_name": "Cubic Meter", "uom_symbol": "m³", "uom_type": "Volume", "must_be_whole_number": 0, "enabled": 1, "description": "Volume in cubic meters"},
	
	# Length
	{"uom_name": "Meter", "uom_symbol": "m", "uom_type": "Length", "must_be_whole_number": 0, "enabled": 1, "description": "Length in meters"},
	{"uom_name": "Centimeter", "uom_symbol": "cm", "uom_type": "Length", "must_be_whole_number": 0, "enabled": 1, "description": "Length in centimeters"},
	{"uom_name": "Millimeter", "uom_symbol": "mm", "uom_type": "Length", "must_be_whole_number": 0, "enabled": 1, "description": "Length in millimeters"},
	{"uom_name": "Kilometer", "uom_symbol": "km", "uom_type": "Length", "must_be_whole_number": 0, "enabled": 1, "description": "Length in kilometers"},
	{"uom_name": "Inch", "uom_symbol": "in", "uom_type": "Length", "must_be_whole_number": 0, "enabled": 1, "description": "Length in inches"},
	{"uom_name": "Foot", "uom_symbol": "ft", "uom_type": "Length", "must_be_whole_number": 0, "enabled": 1, "description": "Length in feet"},
	
	# Area
	{"uom_name": "Square Meter", "uom_symbol": "m²", "uom_type": "Area", "must_be_whole_number": 0, "enabled": 1, "description": "Area in square meters"},
	{"uom_name": "Square Foot", "uom_symbol": "ft²", "uom_type": "Area", "must_be_whole_number": 0, "enabled": 1, "description": "Area in square feet"},
	
	# Special
	{"uom_name": "Roll", "uom_symbol": "Roll", "uom_type": "Other", "must_be_whole_number": 1, "enabled": 1, "description": "Roll (cables, wires, fabrics)"},
	{"uom_name": "Sheet", "uom_symbol": "Sht", "uom_type": "Other", "must_be_whole_number": 1, "enabled": 1, "description": "Sheet (paper, metal sheets)"},
	{"uom_name": "Hour", "uom_symbol": "Hr", "uom_type": "Time", "must_be_whole_number": 0, "enabled": 1, "description": "Time in hours (services)"},
]
