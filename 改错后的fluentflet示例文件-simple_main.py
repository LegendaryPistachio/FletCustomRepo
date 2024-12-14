import flet as ft
from fluentflet.components.background import Background
from fluentflet.components import ( Button, ButtonVariant, 
                                    Checkbox, CheckState,
                                    Slider, SliderOrientation,
                                    Radio, RadioGroup,
                                    TextBox,
                                    Calendar,
                                    Toggle, 
                                    Expander,
                                    Dropdown,
                                    ListItem,
                                    ProgressRing
                                )
from fluentflet.utils import FluentIcon, FluentIcons, FluentIconStyle

class DisplayGroup(ft.Container):
    def __init__(
        self,
        items: list = None,
        **kwargs
    ):
        self.content_column = ft.Column(
            spacing=10,
            horizontal_alignment=ft.CrossAxisAlignment.START,
            expand=True,
        )
        
        if items:
            self.content_column.controls.extend(items)
        
        super().__init__(
            content=self.content_column,
            padding=0,
            border_radius=8,
            expand=True,
            **kwargs
        )

    def add(self, item):
        """Add a DisplayItem to the group"""
        self.content_column.controls.append(item)
        self.update()

    def remove(self, item):
        """Remove a DisplayItem from the group"""
        self.content_column.controls.remove(item)
        self.update()

    def clear(self):
        """Remove all DisplayItems"""
        self.content_column.controls.clear()
        self.update()
        
class DisplayItem(ft.Container):
    def __init__(
        self,
        title: str = "",
        content: ft.Control = None,
        **kwargs
    ):
        self.title = ft.Text(
            value=title,
            size=16,
            weight=ft.FontWeight.W_500
        )
        
        self.content_container = ft.Container(
            content=content,
            expand=True
        ) if content else None
        
        super().__init__(
            content=ft.Column(
                [
                    self.title,
                    self.content_container
                ] if content else [self.title],
                spacing=10,
                horizontal_alignment=ft.CrossAxisAlignment.START,
                expand=True
            ),
            padding=20,
            border_radius=8,
            **kwargs
        )
        
class TextBox(ft.TextField):
    def __init__(
        self,
        right_icon: ft.Icon = None,
        right_action=None,
        **kwargs
    ):
        if 'placeholder' in kwargs:
            self.placeholder = kwargs.pop('placeholder')  # 移除 placeholder 以避免传递给父类
        super().__init__(**kwargs)
        if right_icon:
            self.suffix = ft.Row([right_icon], tight=True)
            if right_action:
                right_icon.on_click = right_action

def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.DARK
    page.window.height = 950
    page.window.width = 1600
    page.padding = 5
    page.title = "Fluent Flet"
    page.icon = "fluentflet/static/fluentflet.png"
    page.blur_effect = True

    def on_drag_enter(point):
        print(f"Drag entered at {point}")
        
    def on_drag_over(point):
        print(f"Dragging over {point}")
        
    def on_drag_leave():
        print("Drag left")
        
    def on_files_dropped(files):
        print(f"Got files: {files}")

    page.on_drag_enter = on_drag_enter
    page.on_drag_over = on_drag_over
    page.on_drag_leave = on_drag_leave
    page.on_files_dropped = on_files_dropped
    page.accepts_drops = True

    def increment_value(e):
        current = float(text_value.value) if text_value.value.replace('.','',1).isdigit() else 0
        new_value = min(current + 0.1, 1.0)  # Cap at 1.0
        text_value.value = f"{new_value:.1f}"
        pr.value = new_value
        text_box.value = text_value.value
        page.update()

    # 初始化 text_value
    text_value = TextBox(
        width=200,
        placeholder="0.3",
        right_icon=FluentIcon(FluentIcons.ADD, color="#ffffff", size=14),
        right_action=increment_value,
        on_change=lambda e: setattr(pr, 'value', float(e.data) if e.data.replace('.','',1).isdigit() else pr.value)
    )

    dots_bg = Background.DOTS(width=page.window.width, height=page.window.height)
    content = ft.Stack(
        [
            dots_bg,
            ft.Container(
                content=ft.Column(
                    [
                        ft.Row([
                            ft.Image(page.icon,width=30,height=30),
                            ft.Text("Fluent Flet", size=30, weight=ft.FontWeight.W_900)
                        ]),
                        ft.Row([
                            DisplayGroup([
                                DisplayItem(
                                    title="Buttons",
                                    content=ft.Column([
                                        ft.Row([
                                            Button(content=ft.Text("Button"), on_click=lambda e: print("Button clicked")),
                                            Button("Button", variant=ButtonVariant.ACCENT),
                                            Button("Button", variant=ButtonVariant.TOGGLE),
                                            Button(content=FluentIcon(name=FluentIcons.ADD, size=15)),
                                            Button("Button", variant=ButtonVariant.HYPERLINK),
                                        ]),
                                        ft.Row([
                                            Button(content=ft.Text("Button"), disabled=True),
                                            Button(content=ft.Text("Button"), variant=ButtonVariant.ACCENT, disabled=True),
                                            Button("Button", variant=ButtonVariant.TOGGLE, disabled=True),
                                            Button(content=FluentIcon(name=FluentIcons.ADD, size=15), disabled=True),
                                            Button(content=ft.Text("Button"), variant=ButtonVariant.HYPERLINK, disabled=True)
                                        ])
                                    ], spacing=10)
                                ),
                                DisplayItem(
                                    title="Checkboxes",
                                    content=ft.Column([
                                        Checkbox(label="Two-state Checkbox", on_change=lambda state: print(state)),
                                        Checkbox(label="Three-state Checkbox", three_state=True, on_change=lambda state: print(state)),
                                        Checkbox(label="Three-state (Initially Checked)", state=CheckState.CHECKED, three_state=True, on_change=lambda state: print(state)),
                                        Checkbox(label="Three-state (Initially Indeterminate)", state=CheckState.INDETERMINATE, three_state=True, on_change=lambda state: print(state)),
                                        Checkbox(label="Disabled", disabled=True),
                                        Checkbox(label="Disabled Checked", state=CheckState.CHECKED, disabled=True),
                                        Checkbox(label="Disabled Indeterminate", state=CheckState.INDETERMINATE, disabled=True),
                                    ], spacing=10)
                                ),
                                DisplayItem(
                                    title="Sliders",
                                    content=ft.Row([
                                        Slider(
                                            value=50, 
                                            orientation=SliderOrientation.VERTICAL
                                        ),
                                        Slider(
                                            value=50,
                                            min=0,
                                            max=100,
                                            on_change=lambda e: print(f"Value changed to: {round(e.current_value)}", end="\r")
                                        )
                                    ])
                                )
                            ]),
                            DisplayGroup([
                                DisplayItem(
                                    title="Radio Buttons",
                                    content=RadioGroup(
                                        content=ft.Column([
                                            Radio(value="radio1", label="Option 1"),
                                            Radio(value="radio2", label="Option 2"),
                                            Radio(value="radio3", label="Option 3", disabled=True),
                                        ]),
                                        on_change=lambda value: print("Radio changed:", value)
                                    )
                                ),
                                DisplayItem(
                                    title="TextBox",
                                    content=ft.Column([
                                        TextBox(placeholder="TextBox", width=500, on_change=lambda e: print(e.control.value)),
                                        TextBox(
                                            placeholder="TextBox", 
                                            width=500, 
                                            right_icon=FluentIcon(name=FluentIcons.EYE_SHOW, style=FluentIconStyle.FILLED, size=16), 
                                            password=True
                                        )
                                    ])
                                ),
                                DisplayItem(
                                    title="Expander",
                                    content=ft.Column([
                                        Expander(
                                            header="Basic String Header",
                                            content=ft.Column(
                                                [
                                                    ft.Text("This is some content"),
                                                    Button(ft.Text("Click me"), variant=ButtonVariant.DEFAULT),
                                                ]
                                            ),
                                            expand=True
                                        ),
                                        Expander(
                                            header=ft.Row(
                                                controls=[
                                                    FluentIcon(name=FluentIcons.EDIT_SETTINGS, style=FluentIconStyle.FILLED, size=15, color="#ffffff"),
                                                    ft.Text("Header with Icon"),
                                                ]
                                            ),
                                            content=ft.Text("Content with fancy header"),
                                        ),
                                        Expander(
                                            header=ft.Row(
                                                controls=[
                                                    Checkbox(),
                                                    ft.Text("Header with Action"),
                                                ]
                                            ),
                                            content=ft.Text("Content with fancy header"),
                                        )
                                    ])
                                )
                            ]),
                            DisplayGroup([
                                DisplayItem(
                                    title="Calendar View",
                                    content = ft.Column([
                                        Calendar(
                                            on_select=lambda date: print(f"Date selected: {date.strftime('%Y-%m-%d') if date else 'None'}")
                                        )
                                    ])
                                ),
                                DisplayItem(
                                    title="Dropdown",
                                    content=Dropdown(
                                        options=["Option 1", "Option 2", "Option 3", "Option 4"],
                                        initial_value="Option 1",
                                        max_width=150,
                                        on_select=lambda value: print(f"Selected: {value}")
                                    )
                                ),
                                DisplayItem(
                                    title="Toggle",
                                    content=ft.Column([
                                        Toggle(label="toggle"),
                                        Toggle(
                                            label={
                                                "on_content": "On",
                                                "off_content": "Off"
                                            },
                                            on_change=lambda value: print(value)
                                        ),
                                        Toggle(label="disabled switch", disabled=True)
                                    ])
                                )
                            ]),
                            DisplayGroup([
                                DisplayItem(
                                    title="ListView",
                                    content =ft.ListView(
                                        spacing=2,
                                        padding=0,
                                        controls=[
                                            ListItem(content=ft.Text("Kendall Collins")),
                                            ListItem(content=ft.Text("Henry Ross")),
                                            ListItem(content=ft.Text("Nicole Wagner")),
                                        ]
                                    )
                                ),
                                DisplayItem(
                                    title="Progress Ring",
                                    content = ft.Row([
                                        ProgressRing(),
                                        pr := ProgressRing(value=0.3),
                                        text_box := TextBox(
                                            width=200,
                                            placeholder="0.3",
                                            right_icon=FluentIcon(FluentIcons.ADD, color="#ffffff", size=14),
                                            right_action=increment_value,
                                            on_change=lambda e: setattr(pr, 'value', float(e.data) if e.data.replace('.','',1).isdigit() else pr.value)
                                        )
                                    ])
                                )
                            ])
                        ], spacing=20, expand=True),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.START,
                    spacing=20,
                ),
                padding=20,
                alignment=ft.alignment.top_left,
                expand=True,
            )
        ],
        expand=True
    )

    page.add(content)

    def page_resize(e):
        dots_bg.update()
    page.on_resized = page_resize
    
ft.app(main)