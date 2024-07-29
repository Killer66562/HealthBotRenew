from discord import ButtonStyle, Color, Embed
from discord.ext.commands import Cog
from discord.app_commands.commands import command, describe, rename
from discord.interactions import Interaction

import joblib

from components import \
ButtonWithAnswerView, PrevPageButton, NextPageButton, CallModalButton, ViewNode, \
BMIInputFactory, AgeInputFactory, HBA1CInputFactory, BloodSugarInputFactory, \
AgeModalFactory, BMIModalFactory, HBA1CModalFactory, BloodSugarModalFactory, DiabetesCheckAnswerButton

from predicters import DiabetesPredicter


EMBED_TITLE = "智能健康管家"

BTN_PREV_PAGE = "prev_page"
BTN_NEXT_PAGE = "next_page"
BTN_CALL_MODAL = "call_modal"

ANS_YES = True
ANS_DIABETES = "diabetes"
ANS_MALE = 0
ANS_FEMALE = 1

LABEL_YES = "是"
LABEL_DIABETES = "糖尿病"
LABEL_MALE = "男"
LABEL_FAMALE = "女"

MODEL_URL = "diabete_prediction_model.pkl"

model = joblib.load(MODEL_URL)


class SurveyCog(Cog):
    def __init__(self) -> None:
        super().__init__()

    @command(name="survey", description="填寫問卷")
    async def survey(self, interaction: Interaction, ephemerl: bool = True):
        intro_embed = Embed(title=EMBED_TITLE, description="您好\n我是智能健康管家\n請問您要進行檢測嗎？\n\n填寫過程中\n若有填寫錯誤\n隨時都可以按上一頁或下一頁回頭重填喔！", color=Color.green())
        check_type_embed = Embed(title=EMBED_TITLE, description="請選擇您要檢測的項目。", color=Color.yellow())
        gender_embed = Embed(title=EMBED_TITLE, description="請選擇您的性別。", color=Color.magenta())
        age_embed = Embed(title=EMBED_TITLE, description="請填寫您的年齡。", color=Color.teal())
        bmi_embed = Embed(title=EMBED_TITLE, description="請填寫您的BMI。", color=Color.dark_grey())
        hba1c_embed = Embed(title=EMBED_TITLE, description="請填寫您的糖化血色素值。", color=Color.light_grey())
        blood_sugar_embed = Embed(title=EMBED_TITLE, description="請填寫您的血糖值。", color=Color.purple())
        final_embed = Embed(title=EMBED_TITLE, description="點擊下方按鈕查看結果。", color=Color.gold())

        age_input_factory = AgeInputFactory()
        bmi_input_factory = BMIInputFactory()
        hba1c_input_factory = HBA1CInputFactory()
        blood_sugar_input_factory = BloodSugarInputFactory()

        intro_view = ViewNode(embed=intro_embed)
        check_type_view = ViewNode(prev_view=intro_view, embed=check_type_embed)
        gender_view = ViewNode(prev_view=check_type_view, embed=gender_embed)
        age_view = ViewNode(prev_view=gender_view, embed=age_embed)
        bmi_view = ViewNode(prev_view=age_view, embed=bmi_embed)
        hba1c_view = ViewNode(prev_view=bmi_view, embed=hba1c_embed)
        blood_suger_view = ViewNode(prev_view=hba1c_view, embed=blood_sugar_embed)
        final_view = ViewNode(prev_view=blood_suger_view, embed=final_embed)

        for view in (
            intro_view, 
            check_type_view, 
            gender_view, 
            age_view, 
            bmi_view, 
            hba1c_view, 
            blood_suger_view, 
            final_view
        ):
            prev_page_button = PrevPageButton(answer_view=view, row=1)
            next_page_button = NextPageButton(answer_view=view, row=1)
            call_modal_button = CallModalButton(answer_view=view, row=1)

            view.add_item(prev_page_button)
            view.add_item(next_page_button)
            view.add_item(call_modal_button)
            
            view.register_button(BTN_PREV_PAGE, prev_page_button)
            view.register_button(BTN_NEXT_PAGE, next_page_button)
            view.register_button(BTN_CALL_MODAL, call_modal_button)

        yes_button = ButtonWithAnswerView(answer_view=intro_view, answer=ANS_YES, label=LABEL_YES, style=ButtonStyle.green)

        intro_view.add_item(yes_button)
        intro_view.register_view(ANS_YES, check_type_view)

        diabetes_button = ButtonWithAnswerView(answer_view=check_type_view, answer=ANS_DIABETES, label=LABEL_DIABETES)

        check_type_view.add_item(diabetes_button)
        check_type_view.register_view(ANS_DIABETES, gender_view)

        male_button = ButtonWithAnswerView(answer_view=gender_view, answer=ANS_MALE, label=LABEL_MALE, style=ButtonStyle.blurple)
        female_button = ButtonWithAnswerView(answer_view=gender_view, answer=ANS_FEMALE, label=LABEL_FAMALE, style=ButtonStyle.red)

        gender_view.add_item(male_button)
        gender_view.add_item(female_button)
        gender_view.register_view(ANS_MALE, age_view)
        gender_view.register_view(ANS_FEMALE, age_view)

        age_modal_factory = AgeModalFactory(parent_view=age_view, next_view=bmi_view, text_input_factory=age_input_factory)
        bmi_modal_factory = BMIModalFactory(parent_view=bmi_view, next_view=hba1c_view, text_input_factory=bmi_input_factory)
        hba1c_modal_factory = HBA1CModalFactory(parent_view=hba1c_view, next_view=blood_suger_view, text_input_factory=hba1c_input_factory)
        blood_sugar_modal_factory = BloodSugarModalFactory(parent_view=blood_suger_view, next_view=final_view, text_input_factory=blood_sugar_input_factory)

        age_view.modal_factory = age_modal_factory
        bmi_view.modal_factory = bmi_modal_factory
        hba1c_view.modal_factory = hba1c_modal_factory
        blood_suger_view.modal_factory = blood_sugar_modal_factory

        diabetes_predicter = DiabetesPredicter(model=model)

        diabetes_check_ans_button = DiabetesCheckAnswerButton(start_view=gender_view, predicter=diabetes_predicter, answer_view=final_view, style=ButtonStyle.blurple)

        final_view.add_item(diabetes_check_ans_button)

        return await interaction.response.send_message(view=intro_view, embed=intro_view.embed, ephemeral=ephemerl)