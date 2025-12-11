"""
Generate complete hierarchical demo data for Store Location
3 Warehouses → 3 Zones each → 3 Racks each → 3 Shelves each → 3 Bins each
Total: 3 + 9 + 27 + 81 + 243 = 363 locations
Simpler naming: WH-1, WH-2, WH-3 for easier understanding
"""

def generate_complete_demo_data():
    locations = []
    
    # 3 Warehouses with simple zone naming (A, B, C)
    warehouses = [
        {"code": "WH-1", "zones": ["A", "B", "C"]},
        {"code": "WH-2", "zones": ["A", "B", "C"]},
        {"code": "WH-3", "zones": ["A", "B", "C"]},
    ]
    
    for wh in warehouses:
        wh_code = wh["code"]
        
        # Create Warehouse
        locations.append({
            "location_code": wh_code,
            "location_type": "Warehouse",
            "enabled": 1
        })
        
        # Create Zones for this Warehouse
        for zone_name in wh["zones"]:
            zone_code = f"{wh_code}-{zone_name}"
            
            locations.append({
                "location_code": zone_code,
                "location_type": "Zone",
                "store": wh_code,
                "enabled": 1
            })
            
            # Create 3 Racks for this Zone
            for rack_num in range(1, 4):
                rack_code = f"{zone_code}-R{rack_num:02d}"
                
                locations.append({
                    "location_code": rack_code,
                    "location_type": "Rack",
                    "store": wh_code,
                    "zone": zone_code,
                    "enabled": 1
                })
                
                # Create 3 Shelves for this Rack
                for shelf_num in range(1, 4):
                    shelf_code = f"{rack_code}-S{shelf_num}"
                    
                    locations.append({
                        "location_code": shelf_code,
                        "location_type": "Shelf",
                        "store": wh_code,
                        "zone": zone_code,
                        "rack": rack_code,
                        "enabled": 1
                    })
                    
                    # Create 3 Bins for this Shelf
                    for bin_num in range(1, 4):
                        bin_code = f"{shelf_code}-B{bin_num}"
                        
                        locations.append({
                            "location_code": bin_code,
                            "location_type": "Bin",
                            "store": wh_code,
                            "zone": zone_code,
                            "rack": rack_code,
                            "shelf": shelf_code,
                            "bin": f"B{bin_num}",
                            "enabled": 1
                        })
    
    # Add special locations
    locations.append({"location_code": "TRANSIT", "location_type": "Transit", "enabled": 1})
    locations.append({"location_code": "STAGING", "location_type": "Staging", "enabled": 1})
    
    return locations


if __name__ == "__main__":
    # Generate and save to file
    locations = generate_complete_demo_data()
    
    # Write to Python file
    with open("/home/erpnext/frappe-bench/apps/technical_store_system/technical_store_system/setup/demo_data/store_location.py", "w") as f:
        f.write('"""\n')
        f.write('Store Location Demo Data - COMPLETE HIERARCHY\n')
        f.write('3 Warehouses → 3 Zones each → 3 Racks each → 3 Shelves each → 3 Bins each\n')
        f.write(f'Total locations: {len(locations)}\n')
        f.write('Simpler naming: WH-1, WH-2, WH-3 for easier understanding\n')
        f.write('"""\n\n')
        f.write('DEMO_LOCATIONS = [\n')
        
        for loc in locations:
            f.write('\t' + str(loc) + ',\n')
        
        f.write(']\n')
    
    print(f"✅ Generated {len(locations)} locations")
    print("\nBreakdown:")
    print(f"  Warehouses: 3")
    print(f"  Zones: 9 (3 per warehouse)")
    print(f"  Racks: 27 (3 per zone)")
    print(f"  Shelves: 81 (3 per rack)")
    print(f"  Bins: 243 (3 per shelf)")
    print(f"  Special: 2 (Transit, Staging)")
    print(f"  TOTAL: {len(locations)}")
