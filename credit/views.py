import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .apps import ModelConfig  
from pydantic import BaseModel,ValidationError

class model_input(BaseModel):

    Age: float
    Annual_Income: float
    Monthly_Inhand_Salary: float
    Amount_invested_monthly: float
    Num_Bank_Accounts: float


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
