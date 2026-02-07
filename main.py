import flet as ft
import database as db
import math

def main(page: ft.Page):
    page.title = "Universal Master Calculator"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 1100
    page.window_height = 900
    page.padding = 0
    page.bgcolor = "#f0f2f5"
    page.snack_bar = ft.SnackBar(content=ft.Text("Action Completed!"), bgcolor="green")

    input_style = {
        "border_radius": 8, "content_padding": 15, "text_size": 14, "height": 50,
        "border_color": ft.Colors.GREY_400, "focused_border_color": ft.Colors.INDIGO, "focused_border_width": 2
    }

    # ==========================================
    # 1. UI CONTROLS DEFINITION
    # ==========================================

    # --- A. Main Sign Controls ---
    p_job_name = ft.TextField(label="Job Name / Customer", hint_text="Ex: KBZ Sign", **input_style)
    p_w_ft = ft.TextField(label="ပေ", width=80, keyboard_type=ft.KeyboardType.NUMBER, **input_style)
    p_w_in = ft.TextField(label="လက်မ", width=80, keyboard_type=ft.KeyboardType.NUMBER, **input_style)
    p_h_ft = ft.TextField(label="ပေ", width=80, keyboard_type=ft.KeyboardType.NUMBER, **input_style)
    p_h_in = ft.TextField(label="လက်မ", width=80, keyboard_type=ft.KeyboardType.NUMBER, **input_style)
    p_qty = ft.TextField(label="Qty", width=100, value="1", keyboard_type=ft.KeyboardType.NUMBER, **input_style)
    p_material = ft.Dropdown(label="Select Material", options=[], border_radius=8, content_padding=10)
    p_price = ft.TextField(label="Price", prefix=ft.Text("Ks "), keyboard_type=ft.KeyboardType.NUMBER, **input_style)
    p_res_area = ft.Text("0.00 Sqft", size=16, weight="BOLD", color=ft.Colors.INDIGO_700)
    p_res_amt = ft.Text("0 MMK", size=24, weight="BOLD", color=ft.Colors.GREEN_700)
    p_res_acp = ft.Text("-", size=13, weight="W_500", color=ft.Colors.BLUE_GREY_900)
    p_res_steel = ft.Text("-", size=13, weight="W_500", color=ft.Colors.BLUE_GREY_900)

    # --- B. Acrylic / LED Controls ---
    a_text = ft.TextField(label="Reference Text", hint_text="Ex: KBZ BANK", **input_style)
    a_w_ft = ft.TextField(label="W (ပေ)", width=80, keyboard_type=ft.KeyboardType.NUMBER, **input_style)
    a_w_in = ft.TextField(label="W (လက်မ)", width=80, keyboard_type=ft.KeyboardType.NUMBER, **input_style)
    a_h_ft = ft.TextField(label="H (ပေ)", width=80, keyboard_type=ft.KeyboardType.NUMBER, **input_style)
    a_h_in = ft.TextField(label="H (လက်မ)", width=80, keyboard_type=ft.KeyboardType.NUMBER, **input_style)
    a_depth = ft.TextField(label="Depth (လက်မ)", width=120, keyboard_type=ft.KeyboardType.NUMBER, **input_style)
    a_led_spacing = ft.Dropdown(label="LED Type", options=[ft.dropdown.Option("Module LED (Standard 3\")"), ft.dropdown.Option("Module LED (High Bright 2\")"), ft.dropdown.Option("String/Neon (Normal Font)"), ft.dropdown.Option("String/Neon (Bold/Script)"), ft.dropdown.Option("No LED")], value="Module LED (Standard 3\")", border_radius=8, content_padding=10)
    a_res_block_area = ft.Text("Block Area: 0 Sqft", size=14, color=ft.Colors.GREY_700)
    a_res_actual_need = ft.Text("0 Sqft", size=18, weight="BOLD", color=ft.Colors.ORANGE_900)
    a_res_sheet = ft.Text("-", size=14, color=ft.Colors.GREY_700)
    a_res_side_area = ft.Text("-", size=16, weight="BOLD", color=ft.Colors.PURPLE_700)
    a_res_led_count = ft.Text("-", size=18, weight="BOLD", color=ft.Colors.BLUE_700)
    a_res_led_power = ft.Text("-", size=14, color=ft.Colors.GREY_700)

    # --- C. STICKER Controls ---
    st_w = ft.TextField(label="W (in)", width=90, keyboard_type=ft.KeyboardType.NUMBER, **input_style)
    st_h = ft.TextField(label="H (in)", width=90, keyboard_type=ft.KeyboardType.NUMBER, **input_style)
    st_qty = ft.TextField(label="Qty", width=100, value="100", keyboard_type=ft.KeyboardType.NUMBER, **input_style)
    st_media = ft.Dropdown(label="Media Size", options=[ft.dropdown.Option("Vinyl Roll (4ft / 48\")"), ft.dropdown.Option("Vinyl Roll (3ft / 36\")"), ft.dropdown.Option("Sticker Sheet A3+ (13\"x19\")"), ft.dropdown.Option("Sticker Sheet A4 (8.3\"x11.7\")")], value="Vinyl Roll (4ft / 48\")", border_radius=8, content_padding=10)
    st_price = ft.TextField(label="Price", keyboard_type=ft.KeyboardType.NUMBER, **input_style)
    st_res_total_cost = ft.Text("0 MMK", size=24, weight="BOLD", color=ft.Colors.GREEN_700)
    st_res_unit_cost = ft.Text("Per Pc: 0 MMK", size=14, weight="BOLD", color=ft.Colors.GREEN_900)
    st_res_usage = ft.Text("Usage: -", size=16, weight="BOLD", color=ft.Colors.INDIGO_700)
    st_res_layout = ft.Text("Layout: -", size=14, italic=True, color=ft.Colors.GREY_700)

    # --- D. WEIGHT / COIL Controls ---
    wt_material = ft.Dropdown(label="Material Type", options=[ft.dropdown.Option("Aluminum", data=2.71), ft.dropdown.Option("Stainless Steel", data=7.93), ft.dropdown.Option("Iron", data=7.85), ft.dropdown.Option("Acrylic", data=1.19)], value="Aluminum", border_radius=8, content_padding=10)
    wt_width_mm = ft.TextField(label="Width (mm)", width=120, keyboard_type=ft.KeyboardType.NUMBER, **input_style)
    wt_thick_mm = ft.TextField(label="Thick (mm)", width=120, keyboard_type=ft.KeyboardType.NUMBER, **input_style)
    wt_in_len_ft = ft.TextField(label="Length (ပေ)", width=120, keyboard_type=ft.KeyboardType.NUMBER, **input_style)
    wt_res_kg = ft.Text("0 Kg", size=18, weight="BOLD", color=ft.Colors.BLUE_900)
    wt_in_kg = ft.TextField(label="Weight (Kg)", width=120, keyboard_type=ft.KeyboardType.NUMBER, **input_style)
    wt_res_len = ft.Text("0 Ft", size=18, weight="BOLD", color=ft.Colors.ORANGE_900)
    wt_find_w = ft.TextField(label="Width (ပေ)", width=100, keyboard_type=ft.KeyboardType.NUMBER, **input_style)
    wt_find_h = ft.TextField(label="Height (ပေ)", width=100, keyboard_type=ft.KeyboardType.NUMBER, **input_style)
    wt_find_kg = ft.TextField(label="Total Kg", width=100, keyboard_type=ft.KeyboardType.NUMBER, **input_style)
    wt_res_thick = ft.Text("0 mm", size=18, weight="BOLD", color=ft.Colors.TEAL_700)

    # --- E. WIRE Controls ---
    wr_volts = ft.Dropdown(label="Voltage", width=150, options=[ft.dropdown.Option("12"), ft.dropdown.Option("24"), ft.dropdown.Option("220")], value="12", border_radius=8, content_padding=10)
    wr_watts = ft.TextField(label="Total Power (Watts)", width=200, keyboard_type=ft.KeyboardType.NUMBER, **input_style)
    wr_length = ft.TextField(label="Wire Length (ပေ)", width=200, keyboard_type=ft.KeyboardType.NUMBER, **input_style)
    wr_res_amps = ft.Text("0 A", size=20, weight="BOLD", color=ft.Colors.BLUE_900)
    wr_res_size = ft.Text("-", size=22, weight="BOLD", color=ft.Colors.GREEN_700)
    wr_res_drop = ft.Text("Drop: 0%", size=14, color=ft.Colors.RED_900)
    wr_rev_size = ft.Dropdown(label="Wire Size (mm²)", width=150, options=[ft.dropdown.Option("0.5", data=3), ft.dropdown.Option("0.75", data=6), ft.dropdown.Option("1.0", data=10), ft.dropdown.Option("1.5", data=15), ft.dropdown.Option("2.5", data=20), ft.dropdown.Option("4.0", data=30), ft.dropdown.Option("6.0", data=40), ft.dropdown.Option("10.0", data=60)], value="1.5", border_radius=8, content_padding=10)
    wr_rev_in_load = ft.TextField(label="Load (Watts)", width=120, keyboard_type=ft.KeyboardType.NUMBER, **input_style)
    wr_rev_in_len = ft.TextField(label="Length (ပေ)", width=120, keyboard_type=ft.KeyboardType.NUMBER, **input_style)
    wr_rev_res_len = ft.Text("-", size=16, weight="BOLD", color=ft.Colors.INDIGO_700)
    wr_rev_res_load = ft.Text("-", size=16, weight="BOLD", color=ft.Colors.ORANGE_900)

    # --- F. FURNITURE Controls ---
    f_thick = ft.TextField(label="Thick (in)", width=100, keyboard_type=ft.KeyboardType.NUMBER, **input_style)
    f_width = ft.TextField(label="Width (in)", width=100, keyboard_type=ft.KeyboardType.NUMBER, **input_style)
    f_length = ft.TextField(label="Length (in)", width=100, keyboard_type=ft.KeyboardType.NUMBER, **input_style)
    f_qty = ft.TextField(label="Qty", width=100, value="1", keyboard_type=ft.KeyboardType.NUMBER, **input_style)
    f_price = ft.TextField(label="Price (Per Ton)", prefix=ft.Text("Ks "), keyboard_type=ft.KeyboardType.NUMBER, **input_style)
    f_res_ton = ft.Text("0.0000 Tons", size=18, weight="BOLD", color=ft.Colors.BROWN)
    f_res_amt = ft.Text("0 MMK", size=22, weight="BOLD", color=ft.Colors.GREEN)

    # --- G. ROOFING Controls ---
    e_roof_len = ft.TextField(label="Roof Length (ပေ)", width=200, keyboard_type=ft.KeyboardType.NUMBER, **input_style)
    e_roof_wid = ft.TextField(label="Roof Width (ပေ)", width=200, keyboard_type=ft.KeyboardType.NUMBER, **input_style)
    e_sheet_len = ft.Dropdown(label="Sheet Length", width=200, options=[ft.dropdown.Option("6"), ft.dropdown.Option("8"), ft.dropdown.Option("10"), ft.dropdown.Option("12")], value="10", border_radius=8, content_padding=10)
    e_res_count = ft.Text("0 Sheets", size=22, weight="BOLD", color=ft.Colors.BLUE_900)

    # --- H. COSTING Controls (UPDATED FOR INVOICE) ---
    cp_roll_price = ft.TextField(label="Roll Price (ကျပ်)", prefix=ft.Text("Ks "), keyboard_type=ft.KeyboardType.NUMBER, **input_style)
    cp_len_m = ft.TextField(label="Length (m)", value="70", keyboard_type=ft.KeyboardType.NUMBER, **input_style)
    cp_wid_m = ft.TextField(label="Width (m)", value="1.02", keyboard_type=ft.KeyboardType.NUMBER, **input_style)
    
    cp_ink_cost = ft.TextField(label="Ink Cost (Sqft)", value="0", prefix=ft.Text("Ks "), keyboard_type=ft.KeyboardType.NUMBER, **input_style)
    cp_labor_cost = ft.TextField(label="Overhead (Sqft)", value="0", prefix=ft.Text("Ks "), keyboard_type=ft.KeyboardType.NUMBER, **input_style)
    cp_profit = ft.TextField(label="Profit Margin (%)", value="0", keyboard_type=ft.KeyboardType.NUMBER, **input_style)

    cp_res_sqft_total = ft.Text("Total: 0 Sqft", size=13, color="grey")
    cp_res_base_cost = ft.Text("Base: 0 Ks", size=18, weight="BOLD", color=ft.Colors.BLUE_900)
    cp_res_final_cost = ft.Text("-", size=13, italic=True, color=ft.Colors.GREEN_700)

    # --- I. SETTINGS Controls ---
    s_name = ft.TextField(label="Material Name", width=250, **input_style)
    s_price = ft.TextField(label="Price", width=150, keyboard_type=ft.KeyboardType.NUMBER, **input_style)
    s_table = ft.DataTable(columns=[ft.DataColumn(ft.Text("Name")), ft.DataColumn(ft.Text("Price")), ft.DataColumn(ft.Text("Action"))], rows=[])

    # ==========================================
    # 2. LOGIC FUNCTIONS
    # ==========================================

    def refresh_data():
        all_materials = db.get_all_materials()
        s_table.rows.clear()
        for row in all_materials: s_table.rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text(row[1])), ft.DataCell(ft.Text(f"{row[2]:,.0f}")), ft.DataCell(ft.IconButton(ft.Icons.DELETE, icon_color="red", data=row[1], on_click=delete_material_click))]))
        current_val = p_material.value; p_material.options.clear()
        for row in all_materials: p_material.options.append(ft.dropdown.Option(row[1])) 
        p_material.value = current_val; page.update()

    def fetch_price():
        if p_material.value: p_price.value = str(db.get_material_price(p_material.value))
        p_price.update()

    def on_material_select(e): fetch_price()
    def manual_price_refresh(e): fetch_price()

    # --- CLEAR FUNCTIONS ---
    def clear_sign(e):
        p_job_name.value = ""; p_w_ft.value = ""; p_w_in.value = ""; p_h_ft.value = ""; p_h_in.value = ""; p_qty.value = "1"; p_price.value = ""
        p_res_area.value = "0.00 Sqft"; p_res_amt.value = "0 MMK"; p_res_acp.value = "-"; p_res_steel.value = "-"
        p_job_name.focus(); page.update()

    def clear_acrylic(e):
        a_text.value = ""; a_w_ft.value = ""; a_w_in.value = ""; a_h_ft.value = ""; a_h_in.value = ""; a_depth.value = ""
        a_res_block_area.value = "Block Area: 0 Sqft"; a_res_actual_need.value = "0 Sqft"; a_res_sheet.value = "-"
        a_res_side_area.value = "-"; a_res_led_count.value = "-"; a_res_led_power.value = "-"
        a_text.focus(); page.update()

    def clear_sticker(e):
        st_w.value = ""; st_h.value = ""; st_qty.value = "100"; st_price.value = ""
        st_res_total_cost.value = "0 MMK"; st_res_unit_cost.value = "Per Pc: 0 MMK"; st_res_usage.value = "Usage: -"; st_res_layout.value = "Layout: -"
        st_w.focus(); page.update()

    def clear_weight(e):
        wt_width_mm.value = ""; wt_thick_mm.value = ""; wt_in_len_ft.value = ""; wt_in_kg.value = ""
        wt_find_w.value = ""; wt_find_h.value = ""; wt_find_kg.value = ""
        wt_res_kg.value = "0 Kg"; wt_res_len.value = "0 Ft"; wt_res_thick.value = "0 mm"
        wt_width_mm.focus(); page.update()

    def clear_wire(e):
        wr_watts.value = ""; wr_length.value = ""; wr_rev_in_load.value = ""; wr_rev_in_len.value = ""
        wr_res_amps.value = "0 A"; wr_res_size.value = "-"; wr_res_drop.value = "Drop: 0%"
        wr_rev_res_len.value = "-"; wr_rev_res_load.value = "-"
        wr_watts.focus(); page.update()

    def clear_furniture(e):
        f_thick.value = ""; f_width.value = ""; f_length.value = ""; f_qty.value = "1"; f_price.value = ""
        f_res_ton.value = "0.0000 Tons"; f_res_amt.value = "0 MMK"
        f_thick.focus(); page.update()

    def clear_roof(e):
        e_roof_len.value = ""; e_roof_wid.value = ""
        e_res_count.value = "0 Sheets"
        e_roof_len.focus(); page.update()

    def clear_costing(e):
        cp_roll_price.value = ""; cp_len_m.value = "70"; cp_wid_m.value = "1.02"
        cp_ink_cost.value = "0"; cp_labor_cost.value = "0"; cp_profit.value = "0"
        cp_res_sqft_total.value = "Total: 0 Sqft"; cp_res_base_cost.value = "Base: 0 Ks"; cp_res_final_cost.value = "-"
        cp_roll_price.focus(); page.update()

    # --- CALCULATION LOGIC ---
    def calc_printing(e):
        try:
            wf = float(p_w_ft.value or 0) + (float(p_w_in.value or 0)/12); hf = float(p_h_ft.value or 0) + (float(p_h_in.value or 0)/12)
            q = int(p_qty.value or 1); p = float(p_price.value or 0)
            area = wf * hf; total = area * q * p
            p_res_area.value = f"{area * q:.2f} Sqft"; p_res_amt.value = f"{total:,.0f} MMK"
            acp_sheets = math.ceil(area / 32) * q; p_res_acp.value = f"{acp_sheets} Sheets (4'x8')"
            h_rows = math.ceil(hf / 2) + 1; v_cols = math.ceil(wf / 2) + 1
            steel_bars = math.ceil(((wf * h_rows) + (hf * v_cols)) / 19) * q; p_res_steel.value = f"{steel_bars} Bars (19')"
        except: p_res_amt.value = "Error"; page.update()

    def calc_acrylic(e):
        try:
            wf = float(a_w_ft.value or 0) + (float(a_w_in.value or 0)/12); hf = float(a_h_ft.value or 0) + (float(a_h_in.value or 0)/12)
            depth = float(a_depth.value or 0); text_str = a_text.value.strip()
            if wf == 0 or hf == 0: a_res_block_area.value = "Enter dimensions"; page.update(); return
            block_area_sqft = wf * hf; estimated_usage_sqft = block_area_sqft * 0.6
            a_res_block_area.value = f"Block Area: {block_area_sqft:.2f} Sqft"
            a_res_actual_need.value = f"{estimated_usage_sqft:.2f} Sqft (Face)"; a_res_sheet.value = f"4'x8' Sheet: {(estimated_usage_sqft / 32) * 100:.1f}%"
            perimeter_inches = 0
            if text_str: char_count = len(text_str.replace(" ", "")); factor = 5.5 if "Bold" in a_led_spacing.value else 4.0; perimeter_inches = char_count * (hf * 12) * factor
            if depth > 0 and perimeter_inches > 0: a_res_side_area.value = f"{(perimeter_inches * depth) / 144:.2f} Sqft (Side)"
            else: a_res_side_area.value = "-"
            led_mode = a_led_spacing.value
            if "String/Neon" in led_mode:
                if perimeter_inches > 0: a_res_led_count.value = f"{perimeter_inches/12:.1f} Ft ({perimeter_inches/36:.1f} Yds)"; a_res_led_power.value = f"Based on Text"
                else: a_res_led_count.value = "Enter Text!"; a_res_led_power.value = "-"
            elif "Module LED" in led_mode:
                density = 25 if "High Bright" in led_mode else 16; total_modules = math.ceil(estimated_usage_sqft * density)
                a_res_led_count.value = f"{total_modules} Modules"; a_res_led_power.value = f"Power: ~{total_modules * 1.5:.0f}W"
            else: a_res_led_count.value = "No LED"; a_res_led_power.value = "-"
        except: a_res_actual_need.value = "Error"; page.update()

    def calc_sticker(e):
        try:
            sw = float(st_w.value or 0); sh = float(st_h.value or 0); qty = int(st_qty.value or 0); price = float(st_price.value or 0); media = st_media.value
            if sw == 0 or sh == 0 or qty == 0: st_res_usage.value = "Enter Size & Qty"; page.update(); return
            media_w = 48; is_roll = True
            if "36" in media: media_w = 36
            elif "A3+" in media: media_w = 13; media_h = 19; is_roll = False
            elif "A4" in media: media_w = 8.3; media_h = 11.7; is_roll = False
            margin = 0.5; usable_w = media_w - margin
            if is_roll:
                per_row = max(math.floor(usable_w / sw), math.floor(usable_w / sh))
                if per_row == 0: st_res_usage.value = "Too Big!"; page.update(); return
                row_h = sh if math.floor(usable_w / sw) >= math.floor(usable_w / sh) else sw
                total_len = (math.ceil(qty / per_row) * row_h) / 12
                total_sqft = (total_len * 12 * media_w) / 144
                total_cost = total_sqft * price
                st_res_usage.value = f"Length: {total_len:.2f} Ft"; st_res_layout.value = f"{per_row} per row"
            else:
                usable_h = media_h - margin
                per_sheet = max(math.floor(usable_w/sw)*math.floor(usable_h/sh), math.floor(usable_w/sh)*math.floor(usable_h/sw))
                if per_sheet == 0: st_res_usage.value = "Too Big!"; page.update(); return
                total_sheets = math.ceil(qty / per_sheet)
                total_cost = total_sheets * price
                st_res_usage.value = f"{total_sheets} Sheets"; st_res_layout.value = f"{per_sheet} pcs/sheet"
            st_res_total_cost.value = f"{total_cost:,.0f} MMK"; st_res_unit_cost.value = f"Per Pc: {total_cost / qty:,.1f} MMK"
        except: st_res_usage.value = "Error"; page.update()

    def get_density(mat_name):
        if "Aluminum" in mat_name: return 2.71
        if "Stainless" in mat_name: return 7.93
        if "Iron" in mat_name: return 7.85
        if "Acrylic" in mat_name: return 1.19
        return 1.0

    def calc_weight_from_len(e):
        try:
            width_mm = float(wt_width_mm.value or 0); thick_mm = float(wt_thick_mm.value or 0); length_ft = float(wt_in_len_ft.value or 0); density = get_density(wt_material.value)
            if width_mm == 0 or thick_mm == 0 or length_ft == 0: wt_res_kg.value = "Data?"; page.update(); return
            l_cm = length_ft * 30.48; w_cm = width_mm / 10; t_cm = thick_mm / 10; weight_kg = (l_cm * w_cm * t_cm * density) / 1000
            wt_res_kg.value = f"{weight_kg:.2f} Kg"
        except: wt_res_kg.value = "Error"; page.update()

    def calc_len_from_weight(e):
        try:
            width_mm = float(wt_width_mm.value or 0); thick_mm = float(wt_thick_mm.value or 0); weight_kg = float(wt_in_kg.value or 0); density = get_density(wt_material.value)
            if width_mm == 0 or thick_mm == 0 or weight_kg == 0: wt_res_len.value = "Data?"; page.update(); return
            vol_cm3 = (weight_kg * 1000) / density; w_cm = width_mm / 10; t_cm = thick_mm / 10; l_ft = (vol_cm3 / (w_cm * t_cm)) / 30.48
            wt_res_len.value = f"{l_ft:.1f} Ft"
        except: wt_res_len.value = "Error"; page.update()

    def calc_thick_from_weight(e):
        try:
            wf = float(wt_find_w.value or 0); hf = float(wt_find_h.value or 0); kg = float(wt_find_kg.value or 0); density = get_density(wt_material.value)
            if wf == 0 or hf == 0 or kg == 0: wt_res_thick.value = "Data?"; page.update(); return
            thick_mm = (kg * 10.764) / (density * (wf * hf))
            wt_res_thick.value = f"{thick_mm:.2f} mm"
        except: wt_res_thick.value = "Error"; page.update()

    def calc_wire(e):
        try:
            volts = float(wr_volts.value); watts = float(wr_watts.value or 0); length_ft = float(wr_length.value or 0)
            if watts == 0 or length_ft == 0: wr_res_size.value = "Enter Data"; page.update(); return
            amps = watts / volts; wr_res_amps.value = f"{amps:.2f} A"
            length_m = length_ft * 0.3048; copper_rho = 0.0178; standard_sizes = [0.5, 0.75, 1.0, 1.5, 2.5, 4.0, 6.0, 10.0, 16.0]
            rec_size = None; final_drop_v = 0
            for s in standard_sizes:
                v_drop = (2 * length_m * amps * copper_rho) / s
                if (v_drop / volts) * 100 <= 5.0: rec_size = s; final_drop_v = v_drop; break
            if rec_size: wr_res_size.value = f"Use {rec_size} mm²"; wr_res_drop.value = f"Drop: {final_drop_v:.2f}V ({(final_drop_v/volts)*100:.1f}%)"; wr_res_drop.color = ft.Colors.GREEN_700
            else: wr_res_size.value = "Need > 16 mm²"; wr_res_drop.value = "Unsafe Drop!"; wr_res_drop.color = ft.Colors.RED_700
        except: wr_res_size.value = "Error"; page.update()

    def calc_wire_reverse(e):
        try:
            volts = float(wr_volts.value); size_mm2 = float(wr_rev_size.value)
            amp_limit = 0
            for opt in wr_rev_size.options:
                if opt.key == wr_rev_size.value: amp_limit = opt.data; break
            copper_rho = 0.0178; max_drop_v = volts * 0.05
            if e.control.text == "MAX LENGTH?":
                watts = float(wr_rev_in_load.value or 0)
                if watts == 0: wr_rev_res_len.value = "Enter Load"; page.update(); return
                current = watts / volts
                if current > amp_limit: wr_rev_res_len.value = "UNSAFE LOAD!"; wr_rev_res_len.color = "red"
                else:
                    len_m = (max_drop_v * size_mm2) / (2 * current * copper_rho); len_ft = len_m * 3.28084
                    wr_rev_res_len.value = f"Max {len_ft:.1f} Ft"; wr_rev_res_len.color = ft.Colors.INDIGO_700
            elif e.control.text == "MAX LOAD?":
                length_ft = float(wr_rev_in_len.value or 0)
                if length_ft == 0: wr_rev_res_load.value = "Enter Len"; page.update(); return
                len_m = length_ft * 0.3048; max_current_drop = (max_drop_v * size_mm2) / (2 * len_m * copper_rho)
                final_amps = min(max_current_drop, amp_limit); max_watts = final_amps * volts
                wr_rev_res_load.value = f"Max {max_watts:.0f} W"
        except: wr_rev_res_len.value = "Error"; page.update()

    def calc_furniture(e):
        try:
            vol = (float(f_thick.value or 0) * float(f_width.value or 0) * float(f_length.value or 0)) / 7200
            amt = vol * int(f_qty.value or 1) * float(f_price.value or 0)
            f_res_ton.value = f"{vol * int(f_qty.value or 1):.4f} Tons"
            f_res_amt.value = f"{amt:,.0f} MMK"
        except: pass
        page.update()

    def calc_roofing(e):
        try:
            needed = math.ceil((float(e_roof_len.value or 0) * float(e_roof_wid.value or 0)) / (float(e_sheet_len.value or 10) * 2.5) * 1.1)
            e_res_count.value = f"{needed} pcs (Approx)"
        except: pass
        page.update()

    # --- COSTING CALC (UPDATED) ---
    def calc_detailed_cost(e):
        try:
            roll_price = float(cp_roll_price.value or 0)
            len_m = float(cp_len_m.value or 0)
            wid_m = float(cp_wid_m.value or 0)
            
            ink_cost = float(cp_ink_cost.value or 0)
            labor_cost = float(cp_labor_cost.value or 0)
            profit_pct = float(cp_profit.value or 0)

            if roll_price == 0 or len_m == 0 or wid_m == 0:
                cp_res_base_cost.value = "Enter Data"
                page.update()
                return

            # Area Calculation (Meter to Feet)
            len_ft = len_m * 3.28084
            wid_ft = wid_m * 3.28084
            total_sqft = len_ft * wid_ft
            
            # Base Cost
            base_cost_sqft = roll_price / total_sqft
            
            # Logic: If no extra costs, show ONLY Base Cost prominent
            if ink_cost == 0 and labor_cost == 0 and profit_pct == 0:
                cp_res_sqft_total.value = f"Roll Area: {total_sqft:.1f} Sqft"
                cp_res_base_cost.value = f"Cost: {base_cost_sqft:.0f} Ks/Sqft"
                cp_res_final_cost.value = "-"
            else:
                total_prod_cost = base_cost_sqft + ink_cost + labor_cost
                selling_price = total_prod_cost * (1 + (profit_pct / 100))
                
                cp_res_sqft_total.value = f"Roll Area: {total_sqft:.1f} Sqft"
                cp_res_base_cost.value = f"Base: {base_cost_sqft:.0f} Ks"
                cp_res_final_cost.value = f"Sell: {selling_price:.0f} Ks/Sqft"
                
        except: cp_res_base_cost.value = "Error"; page.update()

    def use_costing_price(e):
        try:
            # Smart extraction: Prefer Base Cost if Sell is empty or dash
            target_str = cp_res_base_cost.value if cp_res_final_cost.value == "-" else cp_res_final_cost.value
            price_str = ''.join(filter(str.isdigit, target_str.split('.')[0])) # Extract numbers
            
            if price_str:
                s_price.value = price_str
                s_price.focus()
                page.update()
                page.open(ft.SnackBar(content=ft.Text(f"Price {price_str} Copied to Settings!"), bgcolor="green"))
        except: pass

    def add_update_click(e):
        if s_name.value and s_price.value: db.upsert_material(s_name.value, float(s_price.value)); s_name.value = ""; s_price.value = ""; s_name.focus(); refresh_data(); page.open(ft.SnackBar(ft.Text("Saved!"), bgcolor="green"))
    def delete_material_click(e): db.delete_material(e.control.data); refresh_data()

    # --- COPY QUOTES ---
    def copy_sign_quote(e):
        job = p_job_name.value or "Sign Project"; w = f"{p_w_ft.value or '0'}' {p_w_in.value or '0'}\""; h = f"{p_h_ft.value or '0'}' {p_h_in.value or '0'}\""
        quote_text = f"""📄 **QUOTATION: {job}**\n------------------------------\n📐 **Size:** {w} x {h}\n🔢 **Qty:** {p_qty.value}\n🛠 **Material:** {p_material.value}\n📏 **Total Area:** {p_res_area.value}\n------------------------------\n💰 **Est. Price:** {p_res_amt.value}\n------------------------------\n*Structure Details:*\n• {p_res_acp.value}\n• {p_res_steel.value}"""
        page.set_clipboard(quote_text); page.open(ft.SnackBar(content=ft.Text("Quotation Copied!"), bgcolor="green"))

    def copy_acrylic_quote(e):
        job = a_text.value or "Acrylic Project"; w = f"{a_w_ft.value or '0'}' {a_w_in.value or '0'}\""; h = f"{a_h_ft.value or '0'}' {a_h_in.value or '0'}\""
        quote_text = f"""💡 **ESTIMATE: {job}**\n------------------------------\n📐 **Block Size:** {w} x {h}\n✨ **Face Area:** {a_res_actual_need.value}\n📦 **3D Side:** {a_res_side_area.value}\n------------------------------\n🛡 **Material Usage:**\n• {a_res_sheet.value}\n------------------------------\n💡 **Lighting:**\n• {a_led_spacing.value}\n• {a_res_led_count.value}\n• {a_res_led_power.value}"""
        page.set_clipboard(quote_text); page.open(ft.SnackBar(content=ft.Text("Estimate Copied!"), bgcolor="green"))

    def copy_sticker_quote(e):
        quote_text = f"""🏷 **STICKER QUOTE**\n------------------------------\n📐 **Size:** {st_w.value}" x {st_h.value}"\n🔢 **Qty:** {st_qty.value} pcs\n🖨 **Media:** {st_media.value}\n------------------------------\n📊 **Usage:** {st_res_usage.value}\nℹ️ **Layout:** {st_res_layout.value}\n------------------------------\n💰 **Total:** {st_res_total_cost.value}\n💵 **Unit Price:** {st_res_unit_cost.value}"""
        page.set_clipboard(quote_text); page.open(ft.SnackBar(content=ft.Text("Copied!"), bgcolor="green"))

    p_material.on_change = on_material_select

    # ==========================================
    # 3. VIEWS CONSTRUCTION
    # ==========================================
    
    # 1. Sign View
    view_sign = ft.Container(content=ft.Column([
            ft.Container(content=ft.Column([
                    ft.Row([ft.Icon(ft.Icons.DASHBOARD_CUSTOMIZE, color=ft.Colors.INDIGO), ft.Text("Signwork Calculator", size=18, weight="BOLD", color=ft.Colors.INDIGO)]), ft.Divider(height=5, color="transparent"),
                    ft.Row([ft.Column([ft.Text("Job Name", size=12, weight="BOLD", color=ft.Colors.BLUE_GREY_800), p_job_name], expand=True)]),
                    ft.Row([ft.Column([ft.Text("W (ft)", size=12, color="grey"), p_w_ft]), ft.Column([ft.Text("W (in)", size=12, color="grey"), p_w_in]), ft.Column([ft.Text("H (ft)", size=12, color="grey"), p_h_ft]), ft.Column([ft.Text("H (in)", size=12, color="grey"), p_h_in])], spacing=10),
                    ft.Row([ft.Column([ft.Text("Qty", size=12, color="grey"), p_qty]), ft.Column([ft.Text("Price", size=12, color="grey"), ft.Row([p_price, ft.IconButton(ft.Icons.REFRESH, on_click=manual_price_refresh, icon_color="blue", tooltip="Refresh")])], expand=True)]),
                    ft.Column([ft.Text("Material", size=12, color="grey"), ft.Container(content=p_material, width=400)]),
                    ft.Row([ft.IconButton(ft.Icons.DELETE_OUTLINE, on_click=clear_sign, icon_color="red", tooltip="Clear"), ft.FilledButton("CALCULATE", on_click=calc_printing, style=ft.ButtonStyle(bgcolor=ft.Colors.INDIGO_600), height=50, expand=True)])
                ], spacing=15), padding=20, bgcolor=ft.Colors.WHITE, border_radius=12, shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.GREY_300)),
            ft.Container(content=ft.Column([ft.Text("COST SUMMARY", size=12, weight="BOLD", color="grey"), ft.Divider(), ft.Row([ft.Text("Area:", size=13), p_res_area], alignment=ft.MainAxisAlignment.SPACE_BETWEEN), ft.Row([ft.Text("Price:", size=13), ft.Row([p_res_amt, ft.IconButton(ft.Icons.COPY, on_click=copy_sign_quote, icon_color="green", icon_size=20)])], alignment=ft.MainAxisAlignment.SPACE_BETWEEN), ft.Divider(), ft.Text("Structure:", size=12, color="grey"), p_res_acp, p_res_steel], spacing=5), padding=20, bgcolor=ft.Colors.WHITE, border_radius=10, shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.GREY_200))
        ], spacing=15, scroll=ft.ScrollMode.HIDDEN), padding=10, expand=True)

    # 2. Acrylic View
    view_acrylic = ft.Container(content=ft.Column([
            ft.Container(content=ft.Column([
                    ft.Row([ft.Icon(ft.Icons.LIGHTBULB_CIRCLE, color=ft.Colors.INDIGO), ft.Text("Acrylic/LED", size=18, weight="BOLD", color=ft.Colors.INDIGO)]), ft.Divider(height=5, color="transparent"),
                    ft.Row([ft.Column([ft.Text("Text", size=12, color="grey"), a_text], expand=True)]),
                    ft.Row([ft.Column([ft.Text("W (ft)", size=12, color="grey"), a_w_ft]), ft.Column([ft.Text("W (in)", size=12, color="grey"), a_w_in]), ft.Column([ft.Text("H (ft)", size=12, color="grey"), a_h_ft]), ft.Column([ft.Text("H (in)", size=12, color="grey"), a_h_in])], spacing=10),
                    ft.Row([ft.Column([ft.Text("Depth", size=12, color="grey"), a_depth]), ft.Column([ft.Text("LED", size=12, color="grey"), ft.Container(content=a_led_spacing, width=250)])], spacing=10),
                    ft.Row([ft.IconButton(ft.Icons.DELETE_OUTLINE, on_click=clear_acrylic, icon_color="red", tooltip="Clear"), ft.FilledButton("CALCULATE", on_click=calc_acrylic, style=ft.ButtonStyle(bgcolor=ft.Colors.ORANGE_700), height=50, expand=True)])
                ], spacing=15), padding=20, bgcolor=ft.Colors.WHITE, border_radius=15, shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.GREY_300)),
            ft.Container(content=ft.Column([ft.Row([ft.Text("ESTIMATE", size=12, weight="BOLD", color="grey"), ft.IconButton(ft.Icons.COPY, on_click=copy_acrylic_quote, icon_color="blue", icon_size=20)], alignment=ft.MainAxisAlignment.SPACE_BETWEEN), ft.Divider(), ft.Row([ft.Text("Face:", size=12), a_res_actual_need], alignment="spaceBetween"), ft.Row([ft.Text("Side:", size=12), a_res_side_area], alignment="spaceBetween"), ft.Divider(), ft.Row([ft.Icon(ft.Icons.LIGHTBULB, size=15), a_res_led_count]), ft.Row([ft.Icon(ft.Icons.POWER, size=15), a_res_led_power])], spacing=5), padding=20, bgcolor=ft.Colors.WHITE, border_radius=15, shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.GREY_200))
        ], spacing=15, scroll=ft.ScrollMode.HIDDEN), padding=10, expand=True)

    # 3. Sticker View
    view_sticker = ft.Container(content=ft.Column([
            ft.Container(content=ft.Column([
                    ft.Row([ft.Icon(ft.Icons.GRID_ON, color=ft.Colors.INDIGO), ft.Text("Sticker Calc", size=18, weight="BOLD", color=ft.Colors.INDIGO)]), ft.Divider(height=5, color="transparent"),
                    ft.Row([ft.Column([ft.Text("W (in)", size=12, color="grey"), st_w]), ft.Column([ft.Text("H (in)", size=12, color="grey"), st_h]), ft.Column([ft.Text("Qty", size=12, color="grey"), st_qty])], spacing=10),
                    ft.Column([ft.Text("Media", size=12, color="grey"), ft.Container(content=st_media, width=400)]),
                    ft.Column([ft.Text("Price", size=12, color="grey"), st_price]),
                    ft.Row([ft.IconButton(ft.Icons.DELETE_OUTLINE, on_click=clear_sticker, icon_color="red"), ft.FilledButton("CALCULATE", on_click=calc_sticker, style=ft.ButtonStyle(bgcolor=ft.Colors.TEAL_700), height=50, expand=True)])
                ], spacing=15), padding=20, bgcolor=ft.Colors.WHITE, border_radius=15, shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.GREY_300)),
            ft.Container(content=ft.Column([ft.Row([ft.Text("RESULT", size=12, weight="BOLD", color="grey"), ft.IconButton(ft.Icons.COPY, on_click=copy_sticker_quote, icon_color="teal", icon_size=20)], alignment=ft.MainAxisAlignment.SPACE_BETWEEN), ft.Divider(), st_res_total_cost, st_res_unit_cost, ft.Divider(), ft.Row([ft.Icon(ft.Icons.STRAIGHTEN, size=15), st_res_usage]), ft.Row([ft.Icon(ft.Icons.GRID_VIEW, size=15), st_res_layout])], spacing=5), padding=20, bgcolor=ft.Colors.WHITE, border_radius=15, shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.GREY_200))
        ], spacing=15, scroll=ft.ScrollMode.HIDDEN), padding=10, expand=True)

    # 4. Weight View
    view_weight = ft.Container(content=ft.Column([
            ft.Container(content=ft.Column([
                    ft.Row([ft.Icon(ft.Icons.SCALE, color=ft.Colors.INDIGO), ft.Text("Coil / Weight", size=18, weight="BOLD", color=ft.Colors.INDIGO)]), ft.Divider(height=5, color="transparent"),
                    ft.Column([ft.Text("Material", size=12, color="grey"), ft.Container(content=wt_material, width=400)]),
                    ft.Row([ft.Column([ft.Text("Width (mm)", size=12, color="grey"), wt_width_mm]), ft.Column([ft.Text("Thick (mm)", size=12, color="grey"), wt_thick_mm])], spacing=10),
                    ft.Divider(),
                    ft.Text("1. Coil Calc", weight="BOLD", color=ft.Colors.INDIGO),
                    ft.Row([ft.Column([ft.Text("Len (ft) -> Kg", size=11), ft.Row([wt_in_len_ft, ft.FilledButton("Kg", on_click=calc_weight_from_len)])]), ft.Column([ft.Text("Kg -> Len (ft)", size=11), ft.Row([wt_in_kg, ft.FilledButton("Ft", on_click=calc_len_from_weight)])])], alignment="spaceBetween"),
                    ft.Row([ft.Container(content=wt_res_kg, bgcolor=ft.Colors.BLUE_50, padding=5, border_radius=5), ft.Container(content=wt_res_len, bgcolor=ft.Colors.ORANGE_50, padding=5, border_radius=5)], alignment="spaceBetween"),
                    ft.Divider(),
                    ft.Text("2. Find Thickness", weight="BOLD", color=ft.Colors.TEAL),
                    ft.Row([ft.Column([ft.Text("W (ft)", size=11), wt_find_w]), ft.Column([ft.Text("H (ft)", size=11), wt_find_h]), ft.Column([ft.Text("Kg", size=11), wt_find_kg])], spacing=5),
                    ft.Row([ft.FilledButton("FIND MM", on_click=calc_thick_from_weight, expand=True), ft.Container(content=wt_res_thick, bgcolor=ft.Colors.TEAL_50, padding=5, border_radius=5)]),
                    ft.Row([ft.IconButton(ft.Icons.DELETE_OUTLINE, on_click=clear_weight, icon_color="red")], alignment=ft.MainAxisAlignment.END)
                ], spacing=10), padding=20, bgcolor=ft.Colors.WHITE, border_radius=15, shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.GREY_300))
        ], spacing=15, scroll=ft.ScrollMode.HIDDEN), padding=10, expand=True)

    # 5. Wire View
    view_wire = ft.Container(content=ft.Column([
            ft.Container(content=ft.Column([
                    ft.Row([ft.Icon(ft.Icons.ELECTRIC_BOLT, color=ft.Colors.INDIGO), ft.Text("Wire Gauge", size=18, weight="BOLD", color=ft.Colors.INDIGO)]), ft.Divider(height=5, color="transparent"),
                    ft.Row([ft.Column([ft.Text("Voltage", size=12, color="grey"), ft.Container(content=wr_volts, width=120)]), ft.Column([ft.Text("Watts", size=12, color="grey"), wr_watts], expand=True)]),
                    ft.Row([ft.Column([ft.Text("Length (ft)", size=12, color="grey"), wr_length], expand=True), ft.FilledButton("CHECK", on_click=calc_wire, height=50)]),
                    ft.Container(content=ft.Column([ft.Row([ft.Text("Current:", size=12), wr_res_amps], alignment="spaceBetween"), ft.Row([ft.Text("Wire:", size=12), wr_res_size], alignment="spaceBetween"), ft.Row([ft.Text("Drop:", size=12), wr_res_drop], alignment="spaceBetween")]), padding=10, bgcolor=ft.Colors.BLUE_50, border_radius=5),
                    ft.Divider(),
                    ft.Text("Safety Check", weight="BOLD", color=ft.Colors.TEAL),
                    ft.Row([ft.Text("Existing Wire:", size=12), wr_rev_size]),
                    ft.Row([ft.Column([ft.Text("Load -> Max Len", size=11), ft.Row([wr_rev_in_load, ft.FilledButton("CALC", on_click=calc_wire_reverse)])]), ft.Container(content=wr_rev_res_len, padding=5)], alignment="spaceBetween"),
                    ft.Row([ft.Column([ft.Text("Len -> Max Load", size=11), ft.Row([wr_rev_in_len, ft.FilledButton("CALC", on_click=calc_wire_reverse)])]), ft.Container(content=wr_rev_res_load, padding=5)], alignment="spaceBetween"),
                    ft.Row([ft.IconButton(ft.Icons.DELETE_OUTLINE, on_click=clear_wire, icon_color="red")], alignment=ft.MainAxisAlignment.END)
                ], spacing=10), padding=20, bgcolor=ft.Colors.WHITE, border_radius=15, shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.GREY_300))
        ], spacing=15, scroll=ft.ScrollMode.HIDDEN), padding=10, expand=True)

    # 6. Furniture View
    view_furn = ft.Container(content=ft.Column([
            ft.Container(content=ft.Column([
                    ft.Row([ft.Icon(ft.Icons.CHAIR, color=ft.Colors.INDIGO), ft.Text("Furniture Calc", size=18, weight="BOLD", color=ft.Colors.INDIGO)]), ft.Divider(height=5, color="transparent"),
                    ft.Row([ft.Column([ft.Text("Thick (in)", size=12, color="grey"), f_thick]), ft.Column([ft.Text("Width (in)", size=12, color="grey"), f_width])], spacing=10),
                    ft.Row([ft.Column([ft.Text("Length (in)", size=12, color="grey"), f_length]), ft.Column([ft.Text("Qty", size=12, color="grey"), f_qty])], spacing=10),
                    ft.Column([ft.Text("Price per Ton", size=12, color="grey"), f_price]),
                    ft.Row([ft.IconButton(ft.Icons.DELETE_OUTLINE, on_click=clear_furniture, icon_color="red"), ft.FilledButton("CALCULATE", on_click=calc_furniture, style=ft.ButtonStyle(bgcolor=ft.Colors.BROWN), height=50, expand=True)])
                ], spacing=15), padding=20, bgcolor=ft.Colors.WHITE, border_radius=15, shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.GREY_300)),
            ft.Container(content=ft.Column([ft.Text("RESULT", size=12, weight="BOLD", color="grey"), ft.Divider(), ft.Row([ft.Text("Volume:", size=13), f_res_ton], alignment="spaceBetween"), ft.Row([ft.Text("Amount:", size=13), f_res_amt], alignment="spaceBetween")], spacing=5), padding=20, bgcolor=ft.Colors.WHITE, border_radius=15, shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.GREY_200))
        ], spacing=15, scroll=ft.ScrollMode.HIDDEN), padding=10, expand=True)

    # 7. Roofing View
    view_roof = ft.Container(content=ft.Column([
            ft.Container(content=ft.Column([
                    ft.Row([ft.Icon(ft.Icons.ROOFING, color=ft.Colors.INDIGO), ft.Text("Roofing Calc", size=18, weight="BOLD", color=ft.Colors.INDIGO)]), ft.Divider(height=5, color="transparent"),
                    ft.Column([ft.Text("Roof Length (ft)", size=12, color="grey"), e_roof_len]),
                    ft.Column([ft.Text("Roof Width (ft)", size=12, color="grey"), e_roof_wid]),
                    ft.Column([ft.Text("Sheet Size (ft)", size=12, color="grey"), ft.Container(content=e_sheet_len, width=400)]),
                    ft.Row([ft.IconButton(ft.Icons.DELETE_OUTLINE, on_click=clear_roof, icon_color="red"), ft.FilledButton("CALCULATE", on_click=calc_roofing, style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE_900), height=50, expand=True)])
                ], spacing=15), padding=20, bgcolor=ft.Colors.WHITE, border_radius=15, shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.GREY_300)),
            ft.Container(content=ft.Row([ft.Icon(ft.Icons.CHECK_CIRCLE, color="blue", size=30), ft.Column([ft.Text("Sheets Needed:", size=12, color="grey"), e_res_count])]), padding=20, bgcolor=ft.Colors.WHITE, border_radius=15, shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.GREY_200))
        ], spacing=15, scroll=ft.ScrollMode.HIDDEN), padding=10, expand=True)

    # 8. Costing View (UPDATED)
    view_costing = ft.Container(content=ft.Column([
            ft.Container(content=ft.Column([
                    ft.Row([ft.Icon(ft.Icons.MONETIZATION_ON, color=ft.Colors.TEAL), ft.Text("Invoice Costing", size=18, weight="BOLD", color=ft.Colors.TEAL)]), ft.Divider(height=5, color="transparent"),
                    ft.Text("1. Invoice Data", weight="BOLD", color=ft.Colors.INDIGO),
                    ft.Row([ft.Column([ft.Text("Length (m)", size=11), cp_len_m]), ft.Column([ft.Text("Width (m)", size=11), cp_wid_m])], spacing=10),
                    ft.Column([ft.Text("Roll Price (Total Amount)", size=12), cp_roll_price]),
                    ft.Divider(),
                    ft.Text("2. Extras (Optional)", weight="BOLD", color=ft.Colors.INDIGO),
                    ft.Row([ft.Column([ft.Text("Ink (Ks)", size=11), cp_ink_cost]), ft.Column([ft.Text("Labor (Ks)", size=11), cp_labor_cost]), ft.Column([ft.Text("Profit %", size=11), cp_profit])], spacing=10),
                    ft.Row([ft.IconButton(ft.Icons.DELETE_OUTLINE, on_click=clear_costing, icon_color="red"), ft.FilledButton("CALC BASE COST", on_click=calc_detailed_cost, style=ft.ButtonStyle(bgcolor=ft.Colors.TEAL_700), height=50, expand=True)]),
                ], spacing=10), padding=20, bgcolor=ft.Colors.WHITE, border_radius=15, shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.GREY_300)),
            ft.Container(content=ft.Column([
                    ft.Row([ft.Text("ANALYSIS", size=12, weight="BOLD", color="grey"), ft.ElevatedButton("USE PRICE", on_click=use_costing_price, icon=ft.Icons.ARROW_FORWARD)], alignment="spaceBetween"),
                    ft.Divider(),
                    cp_res_sqft_total,
                    cp_res_base_cost, # Prominent Base Cost
                    cp_res_final_cost # Optional Sell Price
                ], spacing=5), padding=20, bgcolor=ft.Colors.WHITE, border_radius=15, shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.GREY_200))
        ], spacing=15, scroll=ft.ScrollMode.HIDDEN), padding=10, expand=True)

    # 9. Settings View
    view_settings = ft.Container(content=ft.Column([
            ft.Container(content=ft.Column([
                    ft.Row([ft.Icon(ft.Icons.SETTINGS, color=ft.Colors.INDIGO), ft.Text("Material Database", size=18, weight="BOLD", color=ft.Colors.INDIGO)]), ft.Divider(height=5, color="transparent"),
                    ft.Column([ft.Text("Material Name", size=12, color="grey"), s_name]),
                    ft.Row([ft.Column([ft.Text("Price (per Sqft/Unit)", size=12, color="grey"), s_price], expand=True), ft.IconButton(ft.Icons.SAVE, on_click=add_update_click, icon_color="white", bgcolor="green", width=50, height=50)])
                ], spacing=15), padding=20, bgcolor=ft.Colors.WHITE, border_radius=15, shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.GREY_200)),
            ft.Container(content=s_table, height=400, border=ft.Border.all(1, ft.Colors.GREY_200), border_radius=10, padding=5, bgcolor=ft.Colors.WHITE)
        ], spacing=15, scroll=ft.ScrollMode.HIDDEN), padding=10, expand=True)

    # ==========================================
    # 4. MAIN LAYOUT CONTROLLER
    # ==========================================
    def get_main_view():
        tab_display = ft.Container(content=view_sign, expand=True)
        
        # Tabs
        tabs = [
            ft.OutlinedButton("Signwork", data="sign"),
            ft.OutlinedButton("Acrylic", data="acrylic"),
            ft.OutlinedButton("Sticker", data="sticker"),
            ft.OutlinedButton("Costing", data="cost"),
            ft.OutlinedButton("Weight", data="weight"),
            ft.OutlinedButton("Wire", data="wire"),
            ft.OutlinedButton("Furniture", data="furn"),
            ft.OutlinedButton("Roofing", data="roof"),
            ft.OutlinedButton("Settings", data="set")
        ]

        def switch_tab(e):
            clicked = e.control.data
            for t in tabs: t.style = ft.ButtonStyle(bgcolor=ft.Colors.WHITE, shape=ft.RoundedRectangleBorder(radius=8))
            e.control.style = ft.ButtonStyle(bgcolor=ft.Colors.INDIGO_100, shape=ft.RoundedRectangleBorder(radius=8))
            
            if clicked == "sign": tab_display.content = view_sign
            elif clicked == "acrylic": tab_display.content = view_acrylic
            elif clicked == "sticker": tab_display.content = view_sticker
            elif clicked == "cost": tab_display.content = view_costing
            elif clicked == "weight": tab_display.content = view_weight
            elif clicked == "wire": tab_display.content = view_wire
            elif clicked == "furn": tab_display.content = view_furn
            elif clicked == "roof": tab_display.content = view_roof
            elif clicked == "set": tab_display.content = view_settings
            
            page.update()

        for t in tabs: t.on_click = switch_tab
        tabs[0].style = ft.ButtonStyle(bgcolor=ft.Colors.INDIGO_100, shape=ft.RoundedRectangleBorder(radius=8))

        return ft.Container(content=ft.Column([
            ft.Row(tabs, spacing=5, scroll=ft.ScrollMode.AUTO),
            tab_display
        ]), padding=10)

    page.add(ft.Container(expand=True, content=get_main_view(), padding=0))
    refresh_data()

ft.app(main)