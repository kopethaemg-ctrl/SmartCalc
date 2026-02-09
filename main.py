import flet as ft
import math

# ==========================================
# 1. INTERNAL DATABASE (NO EXTERNAL FILE NEEDED)
# ==========================================
class LocalDB:
    # This simulates your database functions
    @staticmethod
    def get_all_materials():
        return [
            (1, "Vinyl", 800),
            (2, "Sticker", 1200),
            (3, "Acrylic", 4500),
            (4, "Clear Film", 1500)
        ]

    @staticmethod
    def get_material_price(name):
        prices = {"Vinyl": 800, "Sticker": 1200, "Acrylic": 4500, "Clear Film": 1500}
        return prices.get(name, 0)

    @staticmethod
    def upsert_material(name, price):
        print(f"Saved: {name} - {price}") # Simulation

    @staticmethod
    def delete_material(name):
        print(f"Deleted: {name}") # Simulation

# CRITICAL FIX: Assign the class to variable 'db' so existing logic works
db = LocalDB

# ==========================================
# 2. MAIN APP
# ==========================================
def main(page: ft.Page):
    # --- APP CONFIG ---
    page.title = "SmartCalc Pro"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 400
    page.window_height = 800
    page.padding = 0
    page.bgcolor = "#f0f2f5" 
    
    page.theme = ft.Theme(
        color_scheme_seed=ft.Colors.INDIGO,
        visual_density=ft.VisualDensity.COMFORTABLE,
    )

    # --- STYLE HELPERS ---
    def get_input_style(icon, suffix_str=None):
        style = {
            "border_radius": 15,
            "content_padding": 18,
            "text_size": 15,
            "height": 55,
            "bgcolor": ft.Colors.WHITE,
            "border_color": "transparent",
            "focused_border_color": ft.Colors.INDIGO,
            "focused_border_width": 1,
            "prefix_icon": icon,
            "dense": True,
            "expand": True
        }
        if suffix_str:
            style["suffix"] = ft.Text(suffix_str, size=12, color="grey")
        return style

    def get_dropdown_style():
        return {
            "height": 55,
            "border_radius": 15,
            "bgcolor": ft.Colors.WHITE,
            "content_padding": 15,
            "border_color": "transparent",
            "focused_border_color": ft.Colors.INDIGO,
            "focused_border_width": 1,
        }

    card_style = {
        "padding": 25,
        "bgcolor": ft.Colors.WHITE,
        "border_radius": 20,
        "shadow": ft.BoxShadow(blur_radius=20, color=ft.Colors.BLACK12, offset=ft.Offset(0, 5))
    }

    # ==========================================
    # 3. UI CONTROLS definition
    # ==========================================
    
    # SIGNWORK
    p_job = ft.TextField(hint_text="Job Name", **get_input_style(ft.Icons.WORK))
    p_w_ft = ft.TextField(hint_text="W (ft)", keyboard_type=ft.KeyboardType.NUMBER, **get_input_style(ft.Icons.STRAIGHTEN, "ft"))
    p_w_in = ft.TextField(hint_text="W (in)", keyboard_type=ft.KeyboardType.NUMBER, **get_input_style(ft.Icons.SPACE_BAR, "in"))
    p_h_ft = ft.TextField(hint_text="H (ft)", keyboard_type=ft.KeyboardType.NUMBER, **get_input_style(ft.Icons.HEIGHT, "ft"))
    p_h_in = ft.TextField(hint_text="H (in)", keyboard_type=ft.KeyboardType.NUMBER, **get_input_style(ft.Icons.SPACE_BAR, "in"))
    p_qty = ft.TextField(hint_text="Qty", value="1", keyboard_type=ft.KeyboardType.NUMBER, **get_input_style(ft.Icons.NUMBERS))
    p_material = ft.Dropdown(options=[], **get_dropdown_style()) # Options filled later
    p_price = ft.TextField(hint_text="Price", **get_input_style(ft.Icons.MONETIZATION_ON, "Ks"))
    
    p_res_sqft = ft.Text("0 Sqft", size=20, weight="BOLD", color=ft.Colors.INDIGO)
    p_res_price = ft.Text("0 MMK", size=28, weight="BOLD", color=ft.Colors.GREEN)
    p_detail_text = ft.Text("Enter sizes...", size=14, color=ft.Colors.GREY_700)

    # ACRYLIC
    a_w_ft = ft.TextField(hint_text="W (ft)", keyboard_type=ft.KeyboardType.NUMBER, **get_input_style(ft.Icons.STRAIGHTEN, "ft"))
    a_w_in = ft.TextField(hint_text="W (in)", keyboard_type=ft.KeyboardType.NUMBER, **get_input_style(ft.Icons.SPACE_BAR, "in"))
    a_h_ft = ft.TextField(hint_text="H (ft)", keyboard_type=ft.KeyboardType.NUMBER, **get_input_style(ft.Icons.HEIGHT, "ft"))
    a_h_in = ft.TextField(hint_text="H (in)", keyboard_type=ft.KeyboardType.NUMBER, **get_input_style(ft.Icons.SPACE_BAR, "in"))
    a_led = ft.Dropdown(options=[ft.dropdown.Option("Module LED"), ft.dropdown.Option("Neon")], value="Module LED", **get_dropdown_style())
    a_res_main = ft.Text("0 Sqft", size=22, weight="BOLD", color=ft.Colors.ORANGE)
    a_res_sub = ft.Text("-", size=14)
    a_res_led = ft.Text("-", size=14, color=ft.Colors.BLUE)

    # COSTING
    c_roll = ft.TextField(hint_text="Roll Price", keyboard_type=ft.KeyboardType.NUMBER, **get_input_style(ft.Icons.MONEY, "Ks"))
    c_len = ft.TextField(hint_text="Len (m)", value="50", keyboard_type=ft.KeyboardType.NUMBER, **get_input_style(ft.Icons.SQUARE_FOOT, "m"))
    c_wid = ft.TextField(hint_text="Wid (m)", value="1.27", keyboard_type=ft.KeyboardType.NUMBER, **get_input_style(ft.Icons.ASPECT_RATIO, "m"))
    c_ink = ft.TextField(hint_text="Ink Cost", value="50", keyboard_type=ft.KeyboardType.NUMBER, **get_input_style(ft.Icons.WATER_DROP, "Ks"))
    c_lab = ft.TextField(hint_text="Labor", value="50", keyboard_type=ft.KeyboardType.NUMBER, **get_input_style(ft.Icons.ENGINEERING, "Ks"))
    c_prof = ft.TextField(hint_text="Profit %", value="20", keyboard_type=ft.KeyboardType.NUMBER, **get_input_style(ft.Icons.TRENDING_UP, "%"))
    c_res_base = ft.Text("0 Ks", size=16, color=ft.Colors.GREY)
    c_res_final = ft.Text("0 Ks", size=30, weight="BOLD", color=ft.Colors.TEAL)

    # ==========================================
    # 4. LOGIC FUNCTIONS
    # ==========================================
    def refresh_data():
        try:
            # Simulate fetching from DB
            all_materials = db.get_all_materials()
            p_material.options.clear()
            for row in all_materials: 
                # Tuple format: (id, name, price)
                p_material.options.append(ft.dropdown.Option(row[1]))
            page.update()
        except Exception as e:
            print("DB Error:", e)

    def fetch_price(e):
        if p_material.value:
            price = db.get_material_price(p_material.value)
            p_price.value = str(price)
            p_price.update()

    p_material.on_change = fetch_price

    def manual_price_refresh(e):
        fetch_price(e)
        page.snack_bar = ft.SnackBar(ft.Text("Price Updated!"), bgcolor="green")
        page.snack_bar.open = True
        page.update()

    def calc_signwork(e):
        try:
            w = float(p_w_ft.value or 0) + (float(p_w_in.value or 0)/12)
            h = float(p_h_ft.value or 0) + (float(p_h_in.value or 0)/12)
            q = int(p_qty.value or 1); p = float(p_price.value or 0)
            
            if w == 0 or h == 0: return

            sqft = w * h * q
            amt = sqft * p
            
            # Steel Frame
            v_ribs = math.ceil(w / 2) + 1
            h_ribs = math.ceil(h / 2) + 1
            steel_ft = ((h * v_ribs) + (w * h_ribs)) * q
            bars = math.ceil(steel_ft / 19)
            acp = math.ceil(sqft / 32)

            p_res_sqft.value = f"{sqft:.2f} Sqft"
            p_res_price.value = f"{amt:,.0f} MMK"
            p_detail_text.value = f"🔩 Steel (19'): {bars} bars\n🏗️ Grid: {h_ribs} x {v_ribs}\n⬜ ACP: {acp} sheets"
            page.update()
        except: pass

    def calc_acrylic(e):
        try:
            w = float(a_w_ft.value or 0) + (float(a_w_in.value or 0)/12)
            h = float(a_h_ft.value or 0) + (float(a_h_in.value or 0)/12)
            sqft = w * h * 0.6
            sheets = math.ceil(sqft / 32)
            a_res_main.value = f"Est: {sqft:.2f} Sqft"
            a_res_sub.value = f"Sheet: {sheets} (4x8)"
            if "Module" in a_led.value: a_res_led.value = f"LED: ~{math.ceil(sqft * 20)} Mods"
            else: a_res_led.value = "LED: Custom / Neon"
            page.update()
        except: pass

    def calc_costing(e):
        try:
            rp = float(c_roll.value or 0); l = float(c_len.value or 0); w = float(c_wid.value or 0)
            area = l * 3.28 * w * 3.28; base = rp / area
            final = (base + float(c_ink.value) + float(c_lab.value)) * (1 + float(c_prof.value)/100)
            c_res_base.value = f"Base: {base:.0f} Ks"
            c_res_final.value = f"{final:.0f} Ks/Sqft"
            page.update()
        except: pass

    # Clear Functions
    def clear_sign(e):
        p_job.value=""; p_w_ft.value=""; p_w_in.value=""; p_h_ft.value=""; p_h_in.value=""
        p_res_sqft.value="0 Sqft"; p_res_price.value="0 MMK"; p_detail_text.value="..."
        page.update()
    def clear_acrylic(e):
        a_w_ft.value=""; a_w_in.value=""; a_h_ft.value=""; a_h_in.value=""
        a_res_main.value="0 Sqft"; a_res_sub.value="-"; a_res_led.value="-"
        page.update()
    def clear_costing(e):
        c_roll.value=""; c_len.value="50"; c_wid.value="1.27"; c_res_base.value="0 Ks"; c_res_final.value="0 Ks"
        page.update()

    # ==========================================
    # 5. NAVIGATION
    # ==========================================
    def tool_button(title, icon, color, route_name):
        return ft.Container(
            content=ft.Column([
                ft.Icon(icon, size=32, color=ft.Colors.WHITE),
                ft.Text(title, size=13, weight="BOLD", color=ft.Colors.WHITE)
            ], alignment="center", horizontal_alignment="center"),
            width=155, height=100,
            bgcolor=color,
            border_radius=18,
            on_click=lambda _: page.go(route_name),
            shadow=ft.BoxShadow(blur_radius=10, color=color, offset=ft.Offset(0, 4)),
            animate_scale=ft.animation.Animation(100, ft.AnimationCurve.EASE_OUT),
        )

    def view_home():
        return ft.View(
            "/",
            controls=[
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Icon(ft.Icons.CALCULATE, color=ft.Colors.INDIGO, size=30),
                            ft.Text("SmartCalc Pro", size=24, weight="BOLD", color=ft.Colors.INDIGO_900)
                        ], alignment="center"),
                        ft.Divider(height=20, color="transparent"),
                        ft.Text("MAIN TOOLS", size=12, weight="BOLD", color="grey"),
                        ft.Row([
                            tool_button("Sign & Steel", ft.Icons.DASHBOARD_CUSTOMIZE, ft.Colors.INDIGO, "/sign"),
                            tool_button("Acrylic LED", ft.Icons.LIGHTBULB, ft.Colors.ORANGE, "/acrylic"),
                        ], alignment="center"),
                        ft.Divider(height=10, color="transparent"),
                        ft.Row([
                            tool_button("Costing", ft.Icons.MONETIZATION_ON, ft.Colors.GREEN, "/cost"),
                            tool_button("Utilities", ft.Icons.SETTINGS, ft.Colors.BLUE_GREY, "/utils"),
                        ], alignment="center"),
                    ], horizontal_alignment="center"),
                    padding=20
                )
            ],
            bgcolor="#f8f9fa", padding=0
        )

    def view_sign():
        return ft.View(
            "/sign",
            controls=[
                ft.AppBar(title=ft.Text("Sign & Steel", color="white"), bgcolor=ft.Colors.INDIGO, leading=ft.IconButton(ft.Icons.ARROW_BACK, icon_color="white", on_click=lambda _: page.go("/"))),
                ft.Container(content=ft.Column([
                    ft.Container(content=ft.Column([
                        ft.Text("Size Input", weight="BOLD"),
                        p_job,
                        ft.Row([p_w_ft, p_w_in]),
                        ft.Row([p_h_ft, p_h_in]),
                        ft.Row([p_qty, 
                                ft.Container(content=p_price, expand=True),
                                ft.IconButton(ft.Icons.REFRESH, on_click=manual_price_refresh, tooltip="Refresh Price", icon_color="blue")
                               ]),
                        p_material,
                        ft.Row([
                            ft.IconButton(ft.Icons.DELETE_OUTLINE, icon_color="red", on_click=clear_sign, tooltip="Clear"),
                            ft.FilledButton("CALCULATE", on_click=calc_signwork, style=ft.ButtonStyle(bgcolor=ft.Colors.INDIGO, shape=ft.RoundedRectangleBorder(radius=10)), height=50, expand=True)
                        ])
                    ], spacing=10), **card_style),
                    
                    ft.Container(content=ft.Column([
                        ft.Row([ft.Text("Quote Amount", color="grey"), ft.Icon(ft.Icons.ATTACH_MONEY, color="green")], alignment="spaceBetween"),
                        p_res_price,
                        ft.Divider(),
                        ft.Text("Material Estimate", weight="BOLD", color=ft.Colors.INDIGO),
                        ft.Container(content=p_detail_text, bgcolor=ft.Colors.GREY_100, padding=10, border_radius=10)
                    ], spacing=5), **card_style)
                ], spacing=15), padding=20)
            ],
            bgcolor="#f0f2f5", padding=0
        )

    def view_acrylic():
        return ft.View(
            "/acrylic",
            controls=[
                ft.AppBar(title=ft.Text("Acrylic LED", color="white"), bgcolor=ft.Colors.ORANGE, leading=ft.IconButton(ft.Icons.ARROW_BACK, icon_color="white", on_click=lambda _: page.go("/"))),
                ft.Container(content=ft.Column([
                    ft.Container(content=ft.Column([
                        ft.Row([a_w_ft, a_w_in]),
                        ft.Row([a_h_ft, a_h_in]),
                        a_led,
                        ft.Row([
                            ft.IconButton(ft.Icons.DELETE_OUTLINE, icon_color="red", on_click=clear_acrylic, tooltip="Clear"),
                            ft.FilledButton("CALCULATE", on_click=calc_acrylic, style=ft.ButtonStyle(bgcolor=ft.Colors.ORANGE, shape=ft.RoundedRectangleBorder(radius=10)), height=50, expand=True)
                        ])
                    ], spacing=15), **card_style),
                    ft.Container(content=ft.Column([a_res_main, a_res_sub, ft.Divider(), a_res_led]), **card_style)
                ], spacing=15), padding=20)
            ], bgcolor="#f0f2f5", padding=0
        )

    def view_costing():
        return ft.View(
            "/cost",
            controls=[
                ft.AppBar(title=ft.Text("Roll Costing", color="white"), bgcolor=ft.Colors.GREEN, leading=ft.IconButton(ft.Icons.ARROW_BACK, icon_color="white", on_click=lambda _: page.go("/"))),
                ft.Container(content=ft.Column([
                    ft.Container(content=ft.Column([
                        ft.Text("Roll Info", weight="BOLD"),
                        c_roll, ft.Row([c_len, c_wid]),
                        ft.Divider(), ft.Text("Extras", weight="BOLD"),
                        ft.Row([c_ink, c_lab]), c_prof,
                        ft.Row([
                            ft.IconButton(ft.Icons.DELETE_OUTLINE, icon_color="red", on_click=clear_costing, tooltip="Clear"),
                            ft.FilledButton("CALCULATE", on_click=calc_costing, style=ft.ButtonStyle(bgcolor=ft.Colors.GREEN, shape=ft.RoundedRectangleBorder(radius=10)), height=50, expand=True)
                        ])
                    ], spacing=10), **card_style),
                    ft.Container(content=ft.Column([c_res_base, c_res_final], horizontal_alignment="center"), **card_style)
                ], spacing=15), padding=20)
            ], bgcolor="#f0f2f5", padding=0
        )

    def route_change(route):
        page.views.clear()
        page.views.append(view_home()) # Always load home first
        
        if page.route == "/sign":
            page.views.append(view_sign())
        elif page.route == "/acrylic":
            page.views.append(view_acrylic())
        elif page.route == "/cost":
            page.views.append(view_costing())
        elif page.route == "/utils":
             page.views.append(ft.View("/utils", [
                 ft.AppBar(title=ft.Text("Utilities"), leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda _: page.go("/"))),
                 ft.Container(content=ft.Text("More tools coming soon!"), padding=20)
             ]))
        
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    
    # Initialize
    refresh_data()
    page.go("/")

ft.app(target=main)
