import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .apps import HRModelConfig, ModelConfig  
from pydantic import BaseModel,ValidationError
from drf_yasg.utils import swagger_auto_schema

@swagger_auto_schema(
    method='post',
)

class model_input(BaseModel):

    Age: float
    Annual_Income: float
    Monthly_Inhand_Salary: float
    Amount_invested_monthly: float
    Num_Bank_Accounts: float

class hr_model_input(BaseModel):

    CODE_GENDER:float
    CNT_CHILDREN:float
    AMT_INCOME_TOTAL:float
    NAME_EDUCATION_TYPE:float
    NAME_FAMILY_STATUS:float
    NAME_HOUSING_TYPE:float


@csrf_exempt
@require_POST
def calculate_credit_score(request):
    if request.method == 'POST':
        try:
            input_data = json.loads(request.body)
            input_parameters = model_input(**input_data)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format in the request body'}, status=400)
        except ValidationError as e:
            return JsonResponse({'error': f'Invalid data in the request: {e.json()}'}, status=400)

        age = input_parameters.Age
        annual_income = input_parameters.Annual_Income
        monthly_inhand_salary = input_parameters.Monthly_Inhand_Salary
        amount_invested_monthly = input_parameters.Amount_invested_monthly
        num_bank_accounts = input_parameters.Num_Bank_Accounts

        if None in [age, annual_income, monthly_inhand_salary, amount_invested_monthly, num_bank_accounts]:
            return JsonResponse({'error': 'Missing attribute in the request'})

        
        try:
            age = float(age)
            annual_income = float(annual_income)
            monthly_inhand_salary = float(monthly_inhand_salary)
            amount_invested_monthly = float(amount_invested_monthly)
            num_bank_accounts = float(num_bank_accounts)
        except ValueError:
            return JsonResponse({'error': 'Invalid attribute value'})

    
        input_data = [age, annual_income, monthly_inhand_salary, amount_invested_monthly, num_bank_accounts]
        model = ModelConfig.model 
        
        prediction_proba = model.predict_proba([input_data])
        credit_score = model.predict([input_data])
        
        if credit_score[0] == 0:
            return JsonResponse({'credit_score':str(3.33 * prediction_proba[0][0])})
        elif credit_score[0] == 1:
            return JsonResponse({'credit_score':str(3.33 + (3.33 * prediction_proba[0][1]))})
        else:
            return JsonResponse({'credit_score':str(6.66 + (3.33 * prediction_proba[0][2]))})

    return JsonResponse({'error': 'Invalid request method'})


@csrf_exempt
@require_POST
def calculate_hr(request):
    if request.method == 'POST':
        try:
            input_data = json.loads(request.body)
            input_parameters = hr_model_input(**input_data)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format in the request body'}, status=400)
        except ValidationError as e:
            return JsonResponse({'error': f'Invalid data in the request: {e.json()}'}, status=400)

        gender = input_parameters.CODE_GENDER
        count_children = input_parameters.CNT_CHILDREN
        income_total = input_parameters.AMT_INCOME_TOTAL
        education = input_parameters.NAME_EDUCATION_TYPE
        family_status = input_parameters.NAME_FAMILY_STATUS
        housing_type = input_parameters.NAME_HOUSING_TYPE

        if None in [gender, count_children, income_total, education, family_status]:
            return JsonResponse({'error': 'Missing attribute in the request'})

        
        try:
            gender = float(gender)
            count_children = float(count_children)
            income_total = float(income_total)
            education = float(education)
            family_status = float(family_status)
            housing_type = float(housing_type)
        except ValueError:
            return JsonResponse({'error': 'Invalid attribute value'})

    
        input_data = [gender, count_children, income_total, education, family_status,housing_type]
        model = HRModelConfig.model 
        
        prediction_proba = model.predict_proba([input_data])
        hr = model.predict([input_data])
        
        if hr[0]==0:
            return JsonResponse({'hr_prob':str(prediction_proba[0][0])})
        else:
            return JsonResponse({'hr_prob':str(prediction_proba[0][0])})

    return JsonResponse({'error': 'Invalid request method'})
