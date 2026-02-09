# Filename: main.py
import flet as ft
import math
import database as db 

def main(page: ft.Page):
    # --- APP SETTINGS ---
    page.title = "SmartCalc Pro"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 420
    page.window_height = 850
    page.padding = 0
    page.bgcolor = "#f0f2f5" 
    page.window_icon = "logo.png" 
    page.snack_bar = ft.SnackBar(content=ft.Text("Action Completed!"), bgcolor="green")

    # --- STYLES ---
    def get_input_style(icon=None, align=ft.TextAlign.RIGHT):
        return {
            "border_radius": 10,
            "content_padding": 15,
            "text_size": 14,
            "height": 50,
            "bgcolor": "white",
            "border_width": 1,
            "border_color": ft.Colors.BLUE_GREY_100,
            "focused_border_color": ft.Colors.INDIGO_500,
            "focused_border_width": 2,
            "text_align": align,
            "prefix_icon": icon,
            "label_style": ft.TextStyle(size=12, color=ft.Colors.BLUE_GREY_400)
        }

    card_style = {
        "padding": 20,
        "bgcolor": ft.Colors.WHITE,
        "border_radius": 15,
        "border": ft.Border.all(1, ft.Colors.GREY_200)
    }

    # ==========================================
    # 1. DEFINE CONTROLS (Variable Declarations)
    # ==========================================

    # --- A. SIGN CALCULATOR ---
    p_job_name = ft.TextField(label="Customer Name", hint_text="Enter name...", **get_input_style(ft.Icons.PERSON, ft.TextAlign.LEFT))
    p_w_ft = ft.TextField(label="Width (ft)", keyboard_type=ft.KeyboardType.NUMBER, **get_input_style(ft.Icons.WIDTH_FULL))
    p_w_in = ft.TextField(label="Width (in)", keyboard_type=ft.KeyboardType.NUMBER, **get_input_style())
    p_h_ft = ft.TextField(label="Height (ft)", keyboard_type=ft.KeyboardType.NUMBER, **get_input_style(ft.Icons.HEIGHT))
    p_h_in = ft.TextField(label="Height (in)", keyboard_type=ft.KeyboardType.NUMBER, **get_input_style())
    p_qty = ft.TextField(label="Qty", value="1", keyboard_type=ft.KeyboardType.NUMBER, **get_input_style(ft.Icons.NUMBERS))
    p_material = ft.Dropdown(label="Select Material", options=[], border_radius=10, content_padding=12, height=50, bgcolor="white", focused_border_color=ft.Colors.INDIGO_500, expand=True)
    p_price = ft.TextField(label="Price (Ks)", prefix=ft.Text("Ks "), keyboard_type=ft.KeyboardType.NUMBER, expand=True, **get_input_style(ft.Icons.MONETIZATION_ON))
    
    p_res_area = ft.Text("0.00", size=24, weight="BOLD", color=ft.Colors.WHITE)
    p_res_amt = ft.Text("0", size=32, weight="BOLD", color=ft.Colors.WHITE)
    p_res_details = ft.Column([ft.Text("- ACP Sheets", size=12, color=ft.Colors.WHITE54), ft.Text("- Steel Bars", size=12, color=ft.Colors.WHITE54)], spacing=2)

    # --- E. PAINTING CONTROLS (Defined First for Logic) ---
    pt_w = ft.TextField(label="Width (ft)", keyboard_type=ft.KeyboardType.NUMBER, **get_input_style(ft.Icons.WIDTH_FULL))
    pt_h = ft.TextField(label="Height (ft)", keyboard_type=ft.KeyboardType.NUMBER, **get_input_style(ft.Icons.HEIGHT))
    pt_len = ft.TextField(label="Total Length (ft)", keyboard_type=ft.KeyboardType.NUMBER, visible=False, **get_input_style(ft.Icons.LINEAR_SCALE))
    pt_girth = ft.TextField(label="Girth/Perimeter (in)", hint_text="1x1 tube = 4\"", keyboard_type=ft.KeyboardType.NUMBER, visible=False, **get_input_style(ft.Icons.CIRCLE_OUTLINED))
    
    pt_coverage = ft.TextField(label="Coverage (Sqft/Gal)", value="350", keyboard_type=ft.KeyboardType.NUMBER, **get_input_style())
    pt_price = ft.TextField(label="Paint Price (Gal)", keyboard_type=ft.KeyboardType.NUMBER, **get_input_style(ft.Icons.MONETIZATION_ON))
    pt_labor = ft.TextField(label="Labor Cost", value="0", keyboard_type=ft.KeyboardType.NUMBER, **get_input_style())
    pt_profit = ft.TextField(label="Profit (%)", value="0", keyboard_type=ft.KeyboardType.NUMBER, **get_input_style())

    pt_res_paint = ft.Text("0 Gal", size=18, weight="BOLD", color=ft.Colors.ORANGE_900)
    pt_res_cost = ft.Text("0 MMK", size=24, weight="BOLD", color=ft.Colors.GREEN_800)

    # Function for Dropdown Change
    def toggle_paint_mode(e):
        is_surface = pt_type.value == "Surface/Wall (Flat)"
        pt_w.visible = is_surface
        pt_h.visible = is_surface
        pt_len.visible = not is_surface
        pt_girth.visible = not is_surface
        page.update()

    # Paint Dropdown (Initialized without on_change first)
    pt_type = ft.Dropdown(
        label="Painting Mode", 
        options=[ft.dropdown.Option("Surface/Wall (Flat)"), ft.dropdown.Option("Steel Frame (Spray)")], 
        value="Surface/Wall (Flat)", 
        border_radius=10, content_padding=12, height=50, bgcolor="white"
    )
    # Assign on_change separately to avoid init error
    pt_type.on_change = toggle_paint_mode

    # --- B. ACRYLIC ---
    a_text = ft.TextField(label="Reference Text", hint_text="Enter Text...", **get_input_style(ft.Icons.TEXT_FIELDS, ft.TextAlign.LEFT))
    a_w_ft = ft.TextField(label="W (ft)", keyboard_type=ft.KeyboardType.NUMBER, **get_input_style())
    a_w_in = ft.TextField(label="W (in)", keyboard_type=ft.KeyboardType.NUMBER, **get_input_style())
    a_h_ft = ft.TextField(label="H (ft)", keyboard_type=ft.KeyboardType.NUMBER, **get_input_style())
    a_h_in = ft.TextField(label="H (in)", keyboard_type=ft.KeyboardType.NUMBER, **get_input_style())
    a_depth = ft.TextField(label="Depth (in)", keyboard_type=ft.KeyboardType.NUMBER, **get_input_style(ft.Icons.LAYERS))
    a_led_spacing = ft.Dropdown(label="LED Type", options=[ft.dropdown.Option("Module LED (Standard 3\")"), ft.dropdown.Option("Module LED (High Bright 2\")"), ft.dropdown.Option("String/Neon (Normal Font)"), ft.dropdown.Option("String/Neon (Bold/Script)"), ft.dropdown.Option("No LED")], value="Module LED (Standard 3\")", border_radius=10, content_padding=12, height=50, bgcolor="white", expand=True)
    
    a_res_actual_need = ft.Text("0 Sqft", size=20, weight="BOLD", color=ft.Colors.ORANGE_900)
    a_res_side_area = ft.Text("-", size=14, weight="BOLD", color=ft.Colors.PURPLE_700)
    a_res_led_count = ft.Text("-", size=14, weight="BOLD", color=ft.Colors.BLUE_700)
    a_res_led_power = ft.Text("-", size=12, color=ft.Colors.GREY_700)

    # --- C. STICKER ---
    st_w = ft.TextField(label="W (in)", keyboard_type=ft.KeyboardType.NUMBER, **get_input_style())
    st_h = ft.TextField(label="H (in)", keyboard_type=ft.KeyboardType.NUMBER, **get_input_style())
    st_qty = ft.TextField(label="Qty", value="100", keyboard_type=ft.KeyboardType.NUMBER, **get_input_style())
    st_media = ft.Dropdown(label="Media Size", options=[ft.dropdown.Option("Vinyl Roll (4ft / 48\")"), ft.dropdown.Option("Vinyl Roll (3ft / 36\")"), ft.dropdown.Option("Sticker Sheet A3+ (13\"x19\")"), ft.dropdown.Option("Sticker Sheet A4 (8.3\"x11.7\")")], value="Vinyl Roll (4ft / 48\")", border_radius=10, content_padding=12, bgcolor="white")
    st_price = ft.TextField(label="Price", keyboard_type=ft.KeyboardType.NUMBER, **get_input_style())
    st_res_total_cost = ft.Text("0 MMK", size=20, weight="BOLD", color=ft.Colors.GREEN_700)
    st_res_unit_cost = ft.Text("Per Pc: 0 MMK", size=12, weight="BOLD", color=ft.Colors.GREEN_900)
    st_res_usage = ft.Text("Usage: -", size=14, weight="BOLD", color=ft.Colors.INDIGO_700)
    st_res_layout = ft.Text("Layout: -", size=12, italic=True, color=ft.Colors.GREY_700)

    # --- D. STEEL INSCRIPTION ---
    ss_w = ft.TextField(label="Width (in)", keyboard_type=ft.KeyboardType.NUMBER, **get_input_style())
    ss_h = ft.TextField(label="Height (in)", keyboard_type=ft.KeyboardType.NUMBER, **get_input_style())
    ss_qty = ft.TextField(label="Qty", value="1", keyboard_type=ft.KeyboardType.NUMBER, **get_input_style())
    ss_price = ft.TextField(label="Price (Per Sq.In)", keyboard_type=ft.KeyboardType.NUMBER, **get_input_style(ft.Icons.MONETIZATION_ON))
    ss_res_area = ft.Text("0 Sq.In", size=18, weight="BOLD", color=ft.Colors.BLUE_GREY)
    ss_res_total = ft.Text("0 MMK", size=24, weight="BOLD", color=ft.Colors.GREEN_800)

    # --- F. WEIGHT / COIL ---
    wt_material = ft.Dropdown(label="Material Type", options=[ft.dropdown.Option("Aluminum", data=2.71), ft.dropdown.Option("Stainless Steel", data=7.93), ft.dropdown.Option("Iron", data=7.85), ft.dropdown.Option("Acrylic", data=1.19)], value="Aluminum", border_radius=10, content_padding=12, bgcolor="white")
    wt_width_mm = ft.TextField(label="Width (mm)", keyboard_type=ft.KeyboardType.NUMBER, **get_input_style())
    wt_thick_mm = ft.TextField(label="Thick (mm)", keyboard_type=ft.KeyboardType.NUMBER, **get_input_style())
    wt_in_len_ft = ft.TextField(label="Length (ft)", keyboard_type=ft.KeyboardType.NUMBER, **get_input_style())
    wt_in_kg = ft.TextField(label="Weight (Kg)", keyboard_type=ft.KeyboardType.NUMBER, **get_input_style())
    wt_find_w = ft.TextField(label="W (ft)", keyboard_type=ft.KeyboardType.NUMBER, **get_input_style())
    wt_find_h = ft.TextField(label="H (ft)", keyboard_type=ft.KeyboardType.NUMBER, **get_input_style())
    wt_find_kg = ft.TextField(label="Total Kg", keyboard_type=ft.KeyboardType.NUMBER, **get_input_style())
    wt_res_kg = ft.Text("0 Kg", size=18, weight="BOLD", color=ft.Colors.BLUE_900)
    wt_res_len = ft.Text("0 Ft", size=18, weight="BOLD", color=ft.Colors.ORANGE_900)
    wt_res_thick = ft.Text("0 mm", size=18, weight="BOLD", color=ft.Colors.TEAL_700)

    # --- G. WIRE GAUGE ---
    wr_volts = ft.Dropdown(label="Voltage", options=[ft.dropdown.Option("12"), ft.dropdown.Option("24"), ft.dropdown.Option("220")], value="12", border_radius=10, content_padding=12, bgcolor="white", width=100)
    wr_watts = ft.TextField(label="Power (Watts)", keyboard_type=ft.KeyboardType.NUMBER, **get_input_style())
    wr_length = ft.TextField(label="Length (ft)", keyboard_type=ft.KeyboardType.NUMBER, **get_input_style())
    wr_res_amps = ft.Text("0 A", size=16, weight="BOLD", color=ft.Colors.BLUE_900)
    wr_res_size = ft.Text("-", size=18, weight="BOLD", color=ft.Colors.GREEN_700)
    wr_res_drop = ft.Text("Drop: 0%", size=14, color=ft.Colors.RED_900)
    wr_rev_size = ft.Dropdown(label="Wire Size (mm²)", options=[ft.dropdown.Option("0.5", data=3), ft.dropdown.Option("0.75", data=6), ft.dropdown.Option("1.0", data=10), ft.dropdown.Option("1.5", data=15), ft.dropdown.Option("2.5", data=20), ft.dropdown.Option("4.0", data=30), ft.dropdown.Option("6.0", data=40), ft.dropdown.Option("10.0", data=60)], value="1.5", border_radius=10, content_padding=12, bgcolor="white")
    wr_rev_in_load = ft.TextField(label="Load (W)", keyboard_type=ft.KeyboardType.NUMBER, **get_input_style())
    wr_rev_in_len = ft.TextField(label="Len (ft)", keyboard_type=ft.KeyboardType.NUMBER, **get_input_style())
    wr_rev_res_len = ft.Text("-", size=16, weight="BOLD", color=ft.Colors.INDIGO_700)
    wr_rev_res_load = ft.Text("-", size=16, weight="BOLD", color=ft.Colors.ORANGE_900)

    # --- H. FURNITURE ---
    f_thick = ft.TextField(label="Thick (in)", keyboard_type=ft.KeyboardType.NUMBER, **get_input_style())
    f_width = ft.TextField(label="Width (in)", keyboard_type=ft.KeyboardType.NUMBER, **get_input_style())
    f_length = ft.TextField(label="Length (in)", keyboard_type=ft.KeyboardType.NUMBER, **get_input_style())
    f_qty = ft.TextField(label="Qty", value="1", keyboard_type=ft.KeyboardType.NUMBER, **get_input_style())
    f_price = ft.TextField(label="Price (Ton)", prefix=ft.Text("Ks "), keyboard_type=ft.KeyboardType.NUMBER, **get_input_style())
    f_res_ton = ft.Text("0.0000 Tons", size=18, weight="BOLD", color=ft.Colors.BROWN)
    f_res_amt = ft.Text("0 MMK", size=20, weight="BOLD", color=ft.Colors.GREEN)

    # --- I. ROOFING ---
    e_roof_len = ft.TextField(label="Roof Length (ft)", keyboard_type=ft.KeyboardType.NUMBER, **get_input_style())
    e_roof_wid = ft.TextField(label="Roof Width (ft)", keyboard_type=ft.KeyboardType.NUMBER, **get_input_style())
    e_sheet_len = ft.Dropdown(label="Sheet Length", options=[ft.dropdown.Option("6"), ft.dropdown.Option("8"), ft.dropdown.Option("10"), ft.dropdown.Option("12")], value="10", border_radius=10, content_padding=12, bgcolor="white")
    e_res_count = ft.Text("0 Sheets", size=22, weight="BOLD", color=ft.Colors.BLUE_900)

    # --- J. COSTING ---
    cp_roll_price = ft.TextField(label="Roll Price (Total)", prefix=ft.Text("Ks "), keyboard_type=ft.KeyboardType.NUMBER, **get_input_style())
    cp_len_m = ft.TextField(label="Length (m)", value="70", keyboard_type=ft.KeyboardType.NUMBER, **get_input_style())
    cp_wid_m = ft.TextField(label="Width (m)", value="1.02", keyboard_type=ft.KeyboardType.NUMBER, **get_input_style())
    cp_ink_cost = ft.TextField(label="Ink Cost", suffix=ft.Text("Ks"), value="0", keyboard_type=ft.KeyboardType.NUMBER, **get_input_style())
    cp_labor_cost = ft.TextField(label="Overhead", suffix=ft.Text("Ks"), value="0", keyboard_type=ft.KeyboardType.NUMBER, **get_input_style())
    cp_profit = ft.TextField(label="Profit", suffix=ft.Text("%"), value="0", keyboard_type=ft.KeyboardType.NUMBER, **get_input_style())
    cp_res_sqft_total = ft.Text("0 Sqft", size=14, weight="BOLD", color=ft.Colors.BLUE_GREY)
    cp_res_base_cost = ft.Text("0", size=24, weight="BOLD", color=ft.Colors.INDIGO_800)
    cp_res_final_cost = ft.Text("-", size=14, color=ft.Colors.GREEN_700)

    # --- K. SETTINGS ---
    s_name = ft.TextField(label="Material Name", **get_input_style(ft.Icons.LABEL, ft.TextAlign.LEFT))
    s_price = ft.TextField(label="Price", keyboard_type=ft.KeyboardType.NUMBER, **get_input_style(ft.Icons.MONEY))
    s_table = ft.DataTable(columns=[ft.DataColumn(ft.Text("Name")), ft.DataColumn(ft.Text("Price")), ft.DataColumn(ft.Text("Action"))], rows=[], heading_row_color=ft.Colors.INDIGO_50)

    # ==========================================
    # 2. LOGIC FUNCTIONS
    # ==========================================
    def refresh_data():
        all_materials = db.get_all_materials()
        s_table.rows.clear()
        for row in all_materials: 
            s_table.rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text(row[1])), ft.DataCell(ft.Text(f"{row[2]:,.0f}")), ft.DataCell(ft.IconButton(ft.Icons.DELETE, icon_color="red", data=row[1], on_click=delete_material_click))]))
        current_val = p_material.value
        p_material.options.clear()
        for row in all_materials: p_material.options.append(ft.dropdown.Option(row[1])) 
        if current_val:
            found = False
            for opt in p_material.options:
                if opt.key == current_val: p_material.value = current_val; found = True; break
            if not found and p_material.options: p_material.value = p_material.options[0].key
        page.update()

    def fetch_price(e=None):
        if p_material.value: 
            price = db.get_material_price(p_material.value)
            p_price.value = str(price); p_price.update()
            page.open(ft.SnackBar(content=ft.Text(f"Price updated: {price} Ks"), bgcolor="blue"))
    def on_material_select(e): fetch_price(e)
    def clear_sign(e):
        p_job_name.value = ""; p_w_ft.value = ""; p_w_in.value = ""; p_h_ft.value = ""; p_h_in.value = ""; p_qty.value = "1"; p_price.value = ""
        p_res_area.value = "0.00"; p_res_amt.value = "0"; page.update()
    def clear_acrylic(e): a_text.value = ""; a_w_ft.value = ""; a_w_in.value = ""; a_h_ft.value = ""; a_h_in.value = ""; a_depth.value = ""; a_res_actual_need.value = "0 Sqft"; page.update()
    def clear_sticker(e): st_w.value = ""; st_h.value = ""; st_qty.value = "100"; st_price.value = ""; st_res_total_cost.value = "0 MMK"; page.update()
    def clear_steel(e): ss_w.value = ""; ss_h.value = ""; ss_qty.value = "1"; ss_price.value = ""; ss_res_area.value = "0 Sq.In"; ss_res_total.value = "0 MMK"; page.update()
    def clear_paint(e): pt_w.value = ""; pt_h.value = ""; pt_len.value = ""; pt_girth.value = ""; pt_price.value = ""; pt_labor.value = "0"; pt_profit.value = "0"; pt_res_paint.value = "0 Gal"; pt_res_cost.value = "0 MMK"; page.update()
    def clear_costing(e): cp_roll_price.value = ""; cp_len_m.value = "70"; cp_wid_m.value = "1.02"; cp_ink_cost.value = "0"; cp_labor_cost.value = "0"; cp_profit.value = "0"; cp_res_base_cost.value = "0"; page.update()
    def add_update_click(e): 
        if s_name.value and s_price.value: db.upsert_material(s_name.value, float(s_price.value)); s_name.value = ""; s_price.value = ""; s_name.focus(); refresh_data(); page.open(ft.SnackBar(ft.Text("Saved!"), bgcolor="green"))
    def delete_material_click(e): db.delete_material(e.control.data); refresh_data()
    
    # --- CALCULATIONS ---
    def calc_printing(e):
        try:
            wf = float(p_w_ft.value or 0) + (float(p_w_in.value or 0)/12); hf = float(p_h_ft.value or 0) + (float(p_h_in.value or 0)/12); q = int(p_qty.value or 1); p = float(p_price.value or 0)
            area = wf * hf; total = area * q * p
            p_res_area.value = f"{area * q:.2f}"; p_res_amt.value = f"{total:,.0f}"
            acp_sheets = math.ceil(area / 32) * q; h_rows = math.ceil(hf / 2) + 1; v_cols = math.ceil(wf / 2) + 1; steel_bars = math.ceil(((wf * h_rows) + (hf * v_cols)) / 19) * q
            p_res_details.controls[0].value = f"• ACP Sheets: {acp_sheets} (4'x8')"; p_res_details.controls[1].value = f"• Steel Bars: {steel_bars} (19')"
        except: p_res_amt.value = "Error"; page.update()
        page.update()
    
    def calc_acrylic(e):
        try:
            wf = float(a_w_ft.value or 0) + (float(a_w_in.value or 0)/12); hf = float(a_h_ft.value or 0) + (float(a_h_in.value or 0)/12); depth = float(a_depth.value or 0); text_str = a_text.value.strip()
            if wf == 0 or hf == 0: return
            block_area_sqft = wf * hf; estimated_usage_sqft = block_area_sqft * 0.6; a_res_actual_need.value = f"{estimated_usage_sqft:.2f} Sqft"
            a_res_sheet.value = f"Sheet Usage: {(estimated_usage_sqft / 32) * 100:.1f}% (4'x8')"
            perimeter_inches = 0; 
            if text_str: char_count = len(text_str.replace(" ", "")); factor = 5.5 if "Bold" in a_led_spacing.value else 4.0; perimeter_inches = char_count * (hf * 12) * factor
            if depth > 0 and perimeter_inches > 0: a_res_side_area.value = f"{(perimeter_inches * depth) / 144:.2f} Sqft"
            else: a_res_side_area.value = "-"
            if "Module LED" in a_led_spacing.value:
                density = 25 if "High Bright" in a_led_spacing.value else 16; total_modules = math.ceil(estimated_usage_sqft * density)
                a_res_led_count.value = f"{total_modules} Modules"; a_res_led_power.value = f"Power: ~{total_modules * 1.5:.0f}W"
            else: a_res_led_count.value = "No LED"
        except: pass
        page.update()
    
    def calc_sticker(e):
        try:
            sw = float(st_w.value or 0); sh = float(st_h.value or 0); qty = int(st_qty.value or 0); price = float(st_price.value or 0); media = st_media.value
            if sw == 0 or sh == 0 or qty == 0: return
            media_w = 48; is_roll = True
            if "36" in media: media_w = 36
            elif "A3+" in media: media_w = 13; media_h = 19; is_roll = False
            elif "A4" in media: media_w = 8.3; media_h = 11.7; is_roll = False
            margin = 0.5; usable_w = media_w - margin
            if is_roll:
                per_row = max(math.floor(usable_w / sw), math.floor(usable_w / sh))
                if per_row == 0: st_res_usage.value = "Too Big!"; page.update(); return
                row_h = sh if math.floor(usable_w / sw) >= math.floor(usable_w / sh) else sw
                total_len = (math.ceil(qty / per_row) * row_h) / 12; total_sqft = (total_len * 12 * media_w) / 144; total_cost = total_sqft * price
                st_res_usage.value = f"Length: {total_len:.2f} Ft"; st_res_layout.value = f"{per_row} per row"
            else:
                usable_h = media_h - margin; per_sheet = max(math.floor(usable_w/sw)*math.floor(usable_h/sh), math.floor(usable_w/sh)*math.floor(usable_h/sw))
                if per_sheet == 0: st_res_usage.value = "Too Big!"; page.update(); return
                total_sheets = math.ceil(qty / per_sheet); total_cost = total_sheets * price
                st_res_usage.value = f"{total_sheets} Sheets"; st_res_layout.value = f"{per_sheet} pcs/sheet"
            st_res_total_cost.value = f"{total_cost:,.0f} MMK"; st_res_unit_cost.value = f"Per Pc: {total_cost / qty:,.1f} MMK"
        except: pass
        page.update()

    def calc_steel(e):
        try:
            w = float(ss_w.value or 0); h = float(ss_h.value or 0); q = int(ss_qty.value or 1); p = float(ss_price.value or 0)
            area = w * h; total = area * p * q
            ss_res_area.value = f"Total Area: {area * q:.2f} Sq.In"
            ss_res_total.value = f"{total:,.0f} MMK"
        except: ss_res_total.value = "Error"
        page.update()

    def calc_paint(e):
        try:
            price = float(pt_price.value or 0)
            coverage = float(pt_coverage.value or 350)
            labor = float(pt_labor.value or 0)
            profit = float(pt_profit.value or 0)
            
            sqft = 0
            if pt_type.value == "Surface/Wall (Flat)":
                w = float(pt_w.value or 0)
                h = float(pt_h.value or 0)
                sqft = w * h
            else:
                length = float(pt_len.value or 0)
                girth = float(pt_girth.value or 0)
                base_area = length * (girth / 12)
                sqft = base_area * 1.5 
            
            if sqft > 0:
                gallons = sqft / coverage
                paint_cost = gallons * price
                total_cost = (paint_cost + labor) * (1 + (profit / 100))
                pt_res_paint.value = f"{gallons:.2f} Gal ({sqft:.1f} Sqft)"
                pt_res_cost.value = f"{total_cost:,.0f} MMK"
            else:
                pt_res_paint.value = "0 Gal"; pt_res_cost.value = "0 MMK"
        except: pt_res_cost.value = "Error"
        page.update()

    def calc_detailed_cost(e):
        try:
            roll_price = float(cp_roll_price.value or 0); len_m = float(cp_len_m.value or 0); wid_m = float(cp_wid_m.value or 0)
            ink_cost = float(cp_ink_cost.value or 0); labor_cost = float(cp_labor_cost.value or 0); profit_pct = float(cp_profit.value or 0)
            if roll_price == 0 or len_m == 0 or wid_m == 0: return
            len_ft = len_m * 3.28084; wid_ft = wid_m * 3.28084; total_sqft = len_ft * wid_ft; base_cost_sqft = roll_price / total_sqft
            cp_res_sqft_total.value = f"Total Area: {total_sqft:.1f} Sqft"; cp_res_base_cost.value = f"{base_cost_sqft:.0f} Ks"
            if ink_cost == 0 and labor_cost == 0 and profit_pct == 0: cp_res_final_cost.value = "-"
            else:
                total_prod_cost = base_cost_sqft + ink_cost + labor_cost; selling_price = total_prod_cost * (1 + (profit_pct / 100))
                cp_res_final_cost.value = f"Sell: {selling_price:.0f} Ks/Sqft"
        except: pass
        page.update()
    def use_costing_price(e):
        try:
            target_str = cp_res_base_cost.value if cp_res_final_cost.value == "-" else cp_res_final_cost.value
            price_str = ''.join(filter(str.isdigit, target_str.split('.')[0]))
            if price_str: s_price.value = price_str; s_price.focus(); page.update(); page.open(ft.SnackBar(content=ft.Text(f"Price {price_str} Copied to Settings!"), bgcolor="green"))
        except: pass
    
    # --- WEIGHT ---
    def get_density_val(mat_name):
        if "Aluminum" in mat_name: return 2.71
        if "Stainless" in mat_name: return 7.93
        if "Iron" in mat_name: return 7.85
        if "Acrylic" in mat_name: return 1.19
        return 1.0
    def calc_weight_from_len(e):
        try:
            width_mm = float(wt_width_mm.value or 0); thick_mm = float(wt_thick_mm.value or 0); length_ft = float(wt_in_len_ft.value or 0); density = get_density_val(wt_material.value)
            if width_mm == 0 or thick_mm == 0 or length_ft == 0: return
            l_cm = length_ft * 30.48; w_cm = width_mm / 10; t_cm = thick_mm / 10; weight_kg = (l_cm * w_cm * t_cm * density) / 1000
            wt_res_kg.value = f"{weight_kg:.2f} Kg"
        except: wt_res_kg.value = "Error"; page.update()
        page.update()
    def calc_len_from_weight(e):
        try:
            width_mm = float(wt_width_mm.value or 0); thick_mm = float(wt_thick_mm.value or 0); weight_kg = float(wt_in_kg.value or 0); density = get_density_val(wt_material.value)
            if width_mm == 0 or thick_mm == 0 or weight_kg == 0: return
            vol_cm3 = (weight_kg * 1000) / density; w_cm = width_mm / 10; t_cm = thick_mm / 10; l_ft = (vol_cm3 / (w_cm * t_cm)) / 30.48
            wt_res_len.value = f"{l_ft:.1f} Ft"
        except: wt_res_len.value = "Error"; page.update()
        page.update()
    def calc_thick_from_weight(e):
        try:
            wf = float(wt_find_w.value or 0); hf = float(wt_find_h.value or 0); kg = float(wt_find_kg.value or 0); density = get_density_val(wt_material.value)
            if wf == 0 or hf == 0 or kg == 0: return
            thick_mm = (kg * 10.764) / (density * (wf * hf))
            wt_res_thick.value = f"{thick_mm:.2f} mm"
        except: wt_res_thick.value = "Error"; page.update()
        page.update()

    # --- WIRE ---
    def calc_wire(e):
        try:
            volts = float(wr_volts.value); watts = float(wr_watts.value or 0); length_ft = float(wr_length.value or 0)
            if watts == 0 or length_ft == 0: return
            amps = watts / volts; wr_res_amps.value = f"{amps:.2f} A"
            length_m = length_ft * 0.3048; copper_rho = 0.0178; standard_sizes = [0.5, 0.75, 1.0, 1.5, 2.5, 4.0, 6.0, 10.0, 16.0]
            rec_size = None; final_drop_v = 0
            for s in standard_sizes:
                v_drop = (2 * length_m * amps * copper_rho) / s
                if (v_drop / volts) * 100 <= 5.0: rec_size = s; final_drop_v = v_drop; break
            if rec_size: wr_res_size.value = f"Use {rec_size} mm²"; wr_res_drop.value = f"Drop: {final_drop_v:.2f}V ({(final_drop_v/volts)*100:.1f}%)"; wr_res_drop.color = ft.Colors.GREEN_700
            else: wr_res_size.value = "Need > 16 mm²"; wr_res_drop.value = "Unsafe Drop!"; wr_res_drop.color = ft.Colors.RED_700
        except: pass
        page.update()
    def calc_wire_check(e):
        try:
            volts = float(wr_volts.value); size_mm2 = float(wr_rev_size.value)
            amp_limit = 0
            for opt in wr_rev_size.options:
                if opt.key == wr_rev_size.value: amp_limit = opt.data; break
            copper_rho = 0.0178; max_drop_v = volts * 0.05
            btn_text = e.control.text
            if "LENGTH" in btn_text:
                watts = float(wr_rev_in_load.value or 0)
                if watts == 0: return
                current = watts / volts
                if current > amp_limit: wr_rev_res_len.value = "UNSAFE LOAD!"; wr_rev_res_len.color = "red"
                else:
                    len_m = (max_drop_v * size_mm2) / (2 * current * copper_rho); len_ft = len_m * 3.28084
                    wr_rev_res_len.value = f"Max {len_ft:.1f} Ft"; wr_rev_res_len.color = ft.Colors.INDIGO_700
            else: 
                length_ft = float(wr_rev_in_len.value or 0)
                if length_ft == 0: return
                len_m = length_ft * 0.3048; max_current_drop = (max_drop_v * size_mm2) / (2 * len_m * copper_rho)
                final_amps = min(max_current_drop, amp_limit); max_watts = final_amps * volts
                wr_rev_res_load.value = f"Max {max_watts:.0f} W"
        except: pass
        page.update()

    # --- FURNITURE ---
    def calc_furniture(e):
        try:
            vol = (float(f_thick.value or 0) * float(f_width.value or 0) * float(f_length.value or 0)) / 7200
            amt = vol * int(f_qty.value or 1) * float(f_price.value or 0)
            f_res_ton.value = f"{vol * int(f_qty.value or 1):.4f} Tons"
            f_res_amt.value = f"{amt:,.0f} MMK"
        except: pass
        page.update()

    # --- ROOFING ---
    def calc_roofing(e):
        try:
            needed = math.ceil((float(e_roof_len.value or 0) * float(e_roof_wid.value or 0)) / (float(e_sheet_len.value or 10) * 2.5) * 1.1)
            e_res_count.value = f"{needed} pcs (Approx)"
        except: pass
        page.update()

    # --- COPY QUOTES ---
    def copy_sign_quote(e):
        job = p_job_name.value or "Sign Project"; w = f"{p_w_ft.value or '0'}' {p_w_in.value or '0'}\""; h = f"{p_h_ft.value or '0'}' {p_h_in.value or '0'}\""
        quote_text = f"""📄 **QUOTATION: {job}**\n------------------------------\n📐 **Size:** {w} x {h}\n🔢 **Qty:** {p_qty.value}\n🛠 **Material:** {p_material.value}\n📏 **Total Area:** {p_res_area.value} Sqft\n------------------------------\n💰 **Est. Price:** {p_res_amt.value} MMK\n------------------------------"""
        page.set_clipboard(quote_text); page.open(ft.SnackBar(content=ft.Text("Copied!"), bgcolor="green"))
    def copy_acrylic_quote(e):
        job = a_text.value or "Acrylic Project"; w = f"{a_w_ft.value or '0'}' {a_w_in.value or '0'}\""; h = f"{a_h_ft.value or '0'}' {a_h_in.value or '0'}\""
        quote_text = f"""💡 **ESTIMATE: {job}**\n------------------------------\n📐 **Block Size:** {w} x {h}\n✨ **Face Area:** {a_res_actual_need.value}\n📦 **3D Side:** {a_res_side_area.value}\n------------------------------"""
        page.set_clipboard(quote_text); page.open(ft.SnackBar(content=ft.Text("Copied!"), bgcolor="green"))
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
                    ft.Row([ft.Icon(ft.Icons.DASHBOARD, color=ft.Colors.INDIGO, size=28), ft.Text("Sign Calculator", size=22, weight="BOLD", color=ft.Colors.INDIGO_900)]), 
                    ft.Divider(height=10, color="transparent"),
                    p_job_name,
                    ft.Text("Dimensions", size=14, weight="BOLD", color=ft.Colors.BLUE_GREY),
                    ft.Row([ft.Column([p_w_ft], expand=True), ft.Column([p_w_in], expand=True)], spacing=10),
                    ft.Row([ft.Column([p_h_ft], expand=True), ft.Column([p_h_in], expand=True)], spacing=10),
                    ft.Divider(height=5, color="transparent"),
                    ft.Text("Material & Cost", size=14, weight="BOLD", color=ft.Colors.BLUE_GREY),
                    ft.Row([ft.Icon(ft.Icons.CATEGORY, color=ft.Colors.BLUE_GREY_400), p_material], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row([ft.Column([p_qty], width=100), p_price, ft.IconButton(ft.Icons.SYNC, on_click=fetch_price, icon_color=ft.Colors.INDIGO, bgcolor=ft.Colors.INDIGO_50)], spacing=10),
                    ft.Divider(height=10, color="transparent"),
                    ft.Row([ft.IconButton(ft.Icons.REFRESH, on_click=clear_sign, icon_color=ft.Colors.RED_400), ft.FilledButton("CALCULATE", on_click=calc_printing, style=ft.ButtonStyle(bgcolor=ft.Colors.INDIGO, color="white", shape=ft.RoundedRectangleBorder(radius=10)), height=50, expand=True)])
                ], spacing=12), **card_style),
            ft.Container(content=ft.Column([
                    ft.Row([ft.Text("TOTAL ESTIMATE", size=12, weight="BOLD", color="white"), ft.IconButton(ft.Icons.COPY, on_click=copy_sign_quote, icon_color="white", icon_size=20)], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Divider(color="white"), 
                    ft.Row([ft.Column([ft.Text("Total Amount", size=12, color="white"), ft.Row([p_res_amt, ft.Text("MMK", color="white", size=14, weight="BOLD")])]), ft.Column([ft.Text("Total Area", size=12, color="white"), ft.Row([p_res_area, ft.Text("Sqft", color="white", size=12)])], horizontal_alignment=ft.CrossAxisAlignment.END)], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Divider(color="white"),
                    ft.Text("Structural Requirements:", size=12, weight="BOLD", color="white"),
                    p_res_details
                ], spacing=5), padding=25, border_radius=16, bgcolor=ft.Colors.INDIGO_700)
        ], spacing=20, scroll=ft.ScrollMode.HIDDEN), padding=15, expand=True)

    # 2. Acrylic View
    view_acrylic = ft.Container(content=ft.Column([
            ft.Container(content=ft.Column([
                    ft.Row([ft.Icon(ft.Icons.LIGHTBULB_CIRCLE, color=ft.Colors.ORANGE_700), ft.Text("Acrylic/LED", size=20, weight="BOLD", color=ft.Colors.BLUE_GREY_800)]), 
                    ft.Divider(height=10, color="transparent"),
                    a_text,
                    ft.Divider(height=10, color="transparent"),
                    ft.Row([a_w_ft, a_w_in], spacing=10, expand=True),
                    ft.Row([a_h_ft, a_h_in], spacing=10, expand=True),
                    ft.Divider(height=5, color="transparent"),
                    ft.Row([ft.Container(content=a_depth, expand=1), ft.Row([ft.Icon(ft.Icons.LIGHTBULB, color=ft.Colors.BLUE_GREY_400), a_led_spacing], expand=2)], spacing=10),
                    ft.Divider(height=5, color="transparent"),
                    ft.Row([ft.IconButton(ft.Icons.DELETE_OUTLINE, on_click=clear_acrylic, icon_color="red"), ft.FilledButton("CALCULATE", on_click=calc_acrylic, style=ft.ButtonStyle(bgcolor=ft.Colors.ORANGE_700, color="white", shape=ft.RoundedRectangleBorder(radius=10)), height=50, expand=True)])
                ], spacing=10), **card_style),
            ft.Container(content=ft.Column([
                    ft.Row([ft.Text("ESTIMATE", size=13, weight="BOLD", color=ft.Colors.GREY_600), ft.IconButton(ft.Icons.COPY, on_click=copy_acrylic_quote, icon_color="blue", icon_size=20)], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Divider(), 
                    ft.Row([ft.Text("Face:", size=14), a_res_actual_need], alignment="spaceBetween"),
                    ft.Row([ft.Text("Side:", size=14), a_res_side_area], alignment="spaceBetween"),
                    ft.Divider(),
                    ft.Row([ft.Icon(ft.Icons.LIGHTBULB, size=16, color="orange"), a_res_led_count]),
                    ft.Row([ft.Icon(ft.Icons.POWER, size=16, color="grey"), a_res_led_power])
                ], spacing=5), **card_style)
        ], spacing=15, scroll=ft.ScrollMode.HIDDEN), padding=15, expand=True)

    # 3. Sticker View
    view_sticker = ft.Container(content=ft.Column([
            ft.Container(content=ft.Column([
                    ft.Row([ft.Icon(ft.Icons.GRID_ON, color=ft.Colors.TEAL), ft.Text("Sticker Calc", size=20, weight="BOLD", color=ft.Colors.BLUE_GREY_800)]), ft.Divider(height=5, color="transparent"),
                    ft.Row([st_w, st_h, st_qty], spacing=10),
                    st_media, st_price,
                    ft.Row([ft.IconButton(ft.Icons.DELETE_OUTLINE, on_click=clear_sticker, icon_color="red"), ft.FilledButton("CALCULATE", on_click=calc_sticker, style=ft.ButtonStyle(bgcolor=ft.Colors.TEAL_700, color="white", shape=ft.RoundedRectangleBorder(radius=10)), height=50, expand=True)])
                ], spacing=15), **card_style),
            ft.Container(content=ft.Column([ft.Row([ft.Text("RESULT", size=12, weight="BOLD", color="grey"), ft.IconButton(ft.Icons.COPY, on_click=copy_sticker_quote, icon_color="teal", icon_size=20)], alignment=ft.MainAxisAlignment.SPACE_BETWEEN), ft.Divider(), st_res_total_cost, st_res_unit_cost, ft.Divider(), ft.Row([ft.Icon(ft.Icons.STRAIGHTEN, size=15), st_res_usage]), ft.Row([ft.Icon(ft.Icons.GRID_VIEW, size=15), st_res_layout])], spacing=5), **card_style)
        ], spacing=15, scroll=ft.ScrollMode.HIDDEN), padding=15, expand=True)

    # 4. Steel View
    view_steel = ft.Container(content=ft.Column([
            ft.Container(content=ft.Column([
                    ft.Row([ft.Icon(ft.Icons.SUBTITLES, color=ft.Colors.GREY_700), ft.Text("Steel Inscription", size=20, weight="BOLD", color=ft.Colors.GREY_800)]),
                    ft.Divider(height=5, color="transparent"),
                    ft.Row([ss_w, ss_h], spacing=10),
                    ft.Row([ss_qty, ss_price], spacing=10),
                    ft.Row([
                        ft.IconButton(ft.Icons.DELETE_OUTLINE, on_click=clear_steel, icon_color="red"),
                        ft.FilledButton("CALCULATE", on_click=calc_steel, style=ft.ButtonStyle(bgcolor=ft.Colors.GREY_700, color="white", shape=ft.RoundedRectangleBorder(radius=10)), height=50, expand=True)
                    ])
                ], spacing=15), **card_style),
            ft.Container(content=ft.Column([
                ft.Text("RESULT", size=12, weight="BOLD", color="grey"),
                ft.Divider(),
                ft.Row([ft.Text("Total Area:", size=14), ss_res_area], alignment="spaceBetween"),
                ft.Row([ft.Text("Total Amount:", size=14), ss_res_total], alignment="spaceBetween")
            ], spacing=5), **card_style)
        ], spacing=15, scroll=ft.ScrollMode.HIDDEN), padding=15, expand=True)

    # 5. Painting View
    view_paint = ft.Container(content=ft.Column([
            ft.Container(content=ft.Column([
                    ft.Row([ft.Icon(ft.Icons.FORMAT_PAINT, color=ft.Colors.ORANGE_800), ft.Text("Paint Calc", size=20, weight="BOLD", color=ft.Colors.ORANGE_900)]),
                    ft.Divider(height=5, color="transparent"),
                    pt_type,
                    ft.Row([pt_w, pt_h], spacing=10),
                    ft.Row([pt_len, pt_girth], spacing=10),
                    ft.Text("Cost Estimation", size=14, weight="BOLD", color=ft.Colors.BLUE_GREY),
                    ft.Row([pt_coverage, pt_price], spacing=10),
                    ft.Row([pt_labor, pt_profit], spacing=10),
                    ft.Row([
                        ft.IconButton(ft.Icons.DELETE_OUTLINE, on_click=clear_paint, icon_color="red"),
                        ft.FilledButton("CALCULATE", on_click=calc_paint, style=ft.ButtonStyle(bgcolor=ft.Colors.ORANGE_800, color="white", shape=ft.RoundedRectangleBorder(radius=10)), height=50, expand=True)
                    ])
                ], spacing=15), **card_style),
            ft.Container(content=ft.Column([
                ft.Text("ESTIMATE", size=12, weight="BOLD", color="grey"),
                ft.Divider(),
                ft.Row([ft.Text("Paint Needed:", size=14), pt_res_paint], alignment="spaceBetween"),
                ft.Row([ft.Text("Total Cost:", size=14), pt_res_cost], alignment="spaceBetween")
            ], spacing=5), **card_style)
        ], spacing=15, scroll=ft.ScrollMode.HIDDEN), padding=15, expand=True)

    # 6. Weight View
    view_weight = ft.Container(content=ft.Column([
            ft.Container(content=ft.Column([
                    ft.Row([ft.Icon(ft.Icons.SCALE, color=ft.Colors.BLUE_900), ft.Text("Coil / Weight", size=20, weight="BOLD", color=ft.Colors.BLUE_900)]), ft.Divider(height=5, color="transparent"),
                    wt_material,
                    ft.Row([wt_width_mm, wt_thick_mm], spacing=10),
                    ft.Divider(),
                    ft.Text("1. Coil Calc (Length <-> Kg)", weight="BOLD", color=ft.Colors.BLUE_GREY),
                    ft.Row([ft.Column([wt_in_len_ft, ft.FilledButton("To Kg", on_click=calc_weight_from_len)], expand=True), ft.Column([wt_in_kg, ft.FilledButton("To Ft", on_click=calc_len_from_weight)], expand=True)], spacing=10),
                    ft.Row([ft.Container(content=wt_res_kg, padding=10, bgcolor=ft.Colors.BLUE_50, border_radius=10, expand=True), ft.Container(content=wt_res_len, padding=10, bgcolor=ft.Colors.ORANGE_50, border_radius=10, expand=True)], spacing=10),
                    ft.Divider(),
                    ft.Text("2. Find Thickness (Reverse)", weight="BOLD", color=ft.Colors.BLUE_GREY),
                    ft.Row([wt_find_w, wt_find_h, wt_find_kg], spacing=5),
                    ft.Row([ft.FilledButton("FIND THICKNESS", on_click=calc_thick_from_weight, expand=True), ft.Container(content=wt_res_thick, padding=10, bgcolor=ft.Colors.TEAL_50, border_radius=10)])
                ], spacing=10), **card_style)
        ], spacing=15, scroll=ft.ScrollMode.HIDDEN), padding=15, expand=True)

    # 7. Wire View
    view_wire = ft.Container(content=ft.Column([
            ft.Container(content=ft.Column([
                    ft.Row([ft.Icon(ft.Icons.ELECTRIC_BOLT, color=ft.Colors.YELLOW_800), ft.Text("Wire Gauge", size=20, weight="BOLD", color=ft.Colors.YELLOW_900)]), ft.Divider(height=5, color="transparent"),
                    ft.Row([wr_volts, wr_watts], spacing=10),
                    ft.Row([wr_length, ft.FilledButton("CHECK", on_click=calc_wire, height=50)], spacing=10),
                    ft.Container(content=ft.Column([ft.Row([ft.Text("Current:", size=12), wr_res_amps], alignment="spaceBetween"), ft.Row([ft.Text("Rec. Wire:", size=12), wr_res_size], alignment="spaceBetween"), ft.Row([ft.Text("Voltage Drop:", size=12), wr_res_drop], alignment="spaceBetween")]), padding=15, bgcolor=ft.Colors.YELLOW_50, border_radius=10),
                    ft.Divider(),
                    ft.Text("Safety Check (Max Limit)", weight="BOLD", color=ft.Colors.BLUE_GREY),
                    wr_rev_size,
                    ft.Row([ft.Column([wr_rev_in_load, ft.FilledButton("MAX LENGTH?", on_click=calc_wire_check, width=150)]), ft.Container(content=wr_rev_res_len, padding=10, bgcolor=ft.Colors.INDIGO_50, border_radius=10)], alignment="spaceBetween"),
                    ft.Row([ft.Column([wr_rev_in_len, ft.FilledButton("MAX LOAD?", on_click=calc_wire_check, width=150)]), ft.Container(content=wr_rev_res_load, padding=10, bgcolor=ft.Colors.ORANGE_50, border_radius=10)], alignment="spaceBetween")
                ], spacing=10), **card_style)
        ], spacing=15, scroll=ft.ScrollMode.HIDDEN), padding=15, expand=True)

    # 8. Furniture View
    view_furn = ft.Container(content=ft.Column([
            ft.Container(content=ft.Column([
                    ft.Row([ft.Icon(ft.Icons.CHAIR, color=ft.Colors.BROWN), ft.Text("Furniture Calc", size=20, weight="BOLD", color=ft.Colors.BROWN_800)]), ft.Divider(height=5, color="transparent"),
                    ft.Row([f_thick, f_width], spacing=10),
                    ft.Row([f_length, f_qty], spacing=10),
                    f_price,
                    ft.FilledButton("CALCULATE", on_click=calc_furniture, style=ft.ButtonStyle(bgcolor=ft.Colors.BROWN, color="white", shape=ft.RoundedRectangleBorder(radius=10)), height=50, width=400)
                ], spacing=15), **card_style),
            ft.Container(content=ft.Column([ft.Text("RESULT", size=12, weight="BOLD", color="grey"), ft.Divider(), ft.Row([ft.Text("Volume:", size=14), f_res_ton], alignment="spaceBetween"), ft.Row([ft.Text("Amount:", size=14), f_res_amt], alignment="spaceBetween")], spacing=5), **card_style)
        ], spacing=15, scroll=ft.ScrollMode.HIDDEN), padding=15, expand=True)

    # 9. Roofing View
    view_roof = ft.Container(content=ft.Column([
            ft.Container(content=ft.Column([
                    ft.Row([ft.Icon(ft.Icons.ROOFING, color=ft.Colors.BLUE_GREY), ft.Text("Roofing Calc", size=20, weight="BOLD", color=ft.Colors.BLUE_GREY_800)]), ft.Divider(height=5, color="transparent"),
                    e_roof_len, e_roof_wid, e_sheet_len,
                    ft.FilledButton("CALCULATE", on_click=calc_roofing, style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE_GREY, color="white", shape=ft.RoundedRectangleBorder(radius=10)), height=50, width=400)
                ], spacing=15), **card_style),
            ft.Container(content=ft.Row([ft.Icon(ft.Icons.CHECK_CIRCLE, color="green", size=30), ft.Column([ft.Text("Sheets Needed:", size=12, color="grey"), e_res_count])]), **card_style)
        ], spacing=15, scroll=ft.ScrollMode.HIDDEN), padding=15, expand=True)

    # 10. Costing View
    view_costing = ft.Container(content=ft.Column([
            ft.Container(content=ft.Column([
                    ft.Row([ft.Icon(ft.Icons.MONETIZATION_ON, color=ft.Colors.TEAL), ft.Text("Invoice Costing", size=20, weight="BOLD", color=ft.Colors.TEAL)]), 
                    ft.Divider(height=10, color="transparent"),
                    ft.Container(content=ft.Column([ft.Text("1. Invoice Data", size=14, weight="BOLD", color=ft.Colors.INDIGO_400), ft.Row([cp_len_m, cp_wid_m], spacing=10), cp_roll_price], spacing=10), border=ft.Border.all(1, ft.Colors.GREY_200), border_radius=10, padding=10),
                    ft.Container(content=ft.Column([ft.Text("2. Extras (Optional)", size=14, weight="BOLD", color=ft.Colors.INDIGO_400), ft.Row([cp_ink_cost, cp_labor_cost], spacing=10), cp_profit], spacing=10), border=ft.Border.all(1, ft.Colors.GREY_200), border_radius=10, padding=10),
                    ft.Row([ft.IconButton(ft.Icons.DELETE_OUTLINE, on_click=clear_costing, icon_color="red"), ft.FilledButton("CALC COST", on_click=calc_detailed_cost, style=ft.ButtonStyle(bgcolor=ft.Colors.TEAL_700, color="white", shape=ft.RoundedRectangleBorder(radius=10)), height=50, expand=True)]),
                ], spacing=15), **card_style),
            ft.Container(content=ft.Column([
                    ft.Row([ft.Text("ANALYSIS", size=13, weight="BOLD", color=ft.Colors.GREY_600), ft.FilledButton("USE PRICE", on_click=use_costing_price, icon=ft.Icons.ARROW_UPWARD, style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE_50, color=ft.Colors.BLUE_800))], alignment="spaceBetween"),
                    ft.Divider(),
                    ft.Row([cp_res_sqft_total, cp_res_final_cost], alignment="spaceBetween"),
                    ft.Divider(),
                    ft.Column([ft.Text("Base Cost (Per Sqft):", size=12, color="grey"), ft.Row([cp_res_base_cost, ft.Text("Ks", size=16, color="grey")], alignment="center")], horizontal_alignment="center")
                ], spacing=5), **card_style)
        ], spacing=15, scroll=ft.ScrollMode.HIDDEN), padding=15, expand=True)

    # 11. Settings View
    view_settings = ft.Container(content=ft.Column([
            ft.Container(content=ft.Column([
                    ft.Row([ft.Icon(ft.Icons.SETTINGS, color=ft.Colors.INDIGO), ft.Text("Material Database", size=18, weight="BOLD", color=ft.Colors.INDIGO)]), ft.Divider(height=5, color="transparent"),
                    s_name,
                    ft.Row([s_price, ft.IconButton(ft.Icons.SAVE, on_click=add_update_click, icon_color="white", bgcolor="green", width=50, height=50, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)))], spacing=10)
                ], spacing=15), **card_style),
            ft.Container(content=s_table, height=400, border=ft.Border.all(1, ft.Colors.GREY_200), border_radius=12, padding=5, bgcolor=ft.Colors.WHITE)
        ], spacing=15, scroll=ft.ScrollMode.HIDDEN), padding=15, expand=True)

    # ==========================================
    # 4. MAIN LAYOUT
    # ==========================================
    def get_main_view():
        tab_display = ft.Container(content=view_sign, expand=True)
        nav_items = [
            ("Sign", ft.Icons.DASHBOARD_CUSTOMIZE, "sign"), 
            ("Acrylic", ft.Icons.LIGHTBULB_CIRCLE, "acrylic"), 
            ("Sticker", ft.Icons.GRID_ON, "sticker"), 
            ("Steel", ft.Icons.SUBTITLES, "steel"), 
            ("Paint", ft.Icons.FORMAT_PAINT, "paint"),
            ("Weight", ft.Icons.SCALE, "weight"), 
            ("Wire", ft.Icons.ELECTRIC_BOLT, "wire"), 
            ("Furn", ft.Icons.CHAIR, "furn"), 
            ("Roof", ft.Icons.ROOFING, "roof"), 
            ("Cost", ft.Icons.MONETIZATION_ON, "cost"), 
            ("Set", ft.Icons.SETTINGS, "set")
        ]
        tabs = []
        for title, icon, data in nav_items:
            tabs.append(ft.Container(content=ft.Column([ft.Icon(icon, size=20), ft.Text(title, size=9)], spacing=2, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER), data=data, padding=5, border_radius=10, width=45, on_click=lambda e: switch_tab(e)))

        def switch_tab(e):
            clicked = e.control.data
            for t in tabs: 
                t.bgcolor = ft.Colors.TRANSPARENT; t.content.controls[0].color = ft.Colors.BLUE_GREY_400; t.content.controls[1].color = ft.Colors.BLUE_GREY_400; t.update()
            e.control.bgcolor = ft.Colors.INDIGO_50; e.control.content.controls[0].color = ft.Colors.INDIGO; e.control.content.controls[1].color = ft.Colors.INDIGO; e.control.update()
            
            if clicked == "sign": tab_display.content = view_sign
            elif clicked == "acrylic": tab_display.content = view_acrylic
            elif clicked == "sticker": tab_display.content = view_sticker
            elif clicked == "steel": tab_display.content = view_steel
            elif clicked == "paint": tab_display.content = view_paint
            elif clicked == "weight": tab_display.content = view_weight
            elif clicked == "wire": tab_display.content = view_wire
            elif clicked == "furn": tab_display.content = view_furn
            elif clicked == "roof": tab_display.content = view_roof
            elif clicked == "cost": tab_display.content = view_costing
            elif clicked == "set": tab_display.content = view_settings
            page.update()

        tabs[0].bgcolor = ft.Colors.INDIGO_50; tabs[0].content.controls[0].color = ft.Colors.INDIGO; tabs[0].content.controls[1].color = ft.Colors.INDIGO
        return ft.Container(content=ft.Column([tab_display, ft.Container(content=ft.Row(tabs, scroll=ft.ScrollMode.AUTO), padding=10, bgcolor=ft.Colors.WHITE, border_radius=ft.BorderRadius.only(top_left=20, top_right=20))]), padding=0)

    page.add(ft.Container(expand=True, content=get_main_view(), padding=0))
    refresh_data()

if __name__ == "__main__":
    try:
        ft.app(target=main, assets_dir="assets")
    except:
        ft.run(target=main, assets_dir="assets")
