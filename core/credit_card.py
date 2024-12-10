from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core.models import CreditCard
from account.models import Account
from decimal import Decimal, InvalidOperation


def card_detail(request, card_id):
    account = Account.objects.get(user=request.user)
    credit_card = CreditCard.objects.get(card_id=card_id, user=request.user)

    context = {
        "account": account,
        "credit_card": credit_card,
    }
    return render(request, "credit_card/card-detail.html", context)


# def fund_credit_card(request, card_id):
#     credit_card = CreditCard.objects.get(card_id=card_id, user=request.user)
#     account = request.user.account

#     if request.method == "POST":
#         amount = request.POST.get("funding_amount")

#         if Decimal(amount) <= account.account_balance:
#             account.account_balance -= Decimal(amount)
#             account.save()

#             credit_card.amount += Decimal(amount)
#             credit_card.save()

#             messages.success(request, "Card funded Successfully.")
#             return redirect("core:card-detail", credit_card.card_id)
#         else:
#             messages.warning(request, "Insufficient Funds!")
#             return redirect("core:card-detail", credit_card.card_id)


def fund_credit_card(request, card_id):
    account = Account.objects.get(user=request.user)
    credit_card = CreditCard.objects.get(card_id=card_id, user=request.user)

    if request.method == "POST":
        amount = request.POST.get("funding_amount")
        # print(f"Amount received: {amount}")
        # print(amount)
        try:
            # Validate amount
            if not amount:
                raise ValueError("Amount is required.")
            
            amount = Decimal(amount)
            if account.account_balance >= Decimal(amount):
                credit_card.amount += Decimal(amount)
                credit_card.save()

                account.account_balance -= Decimal(amount)
                account.save()

                messages.success(request, "Card funded Successfully.")
                return redirect("core:card-detail", credit_card.card_id)
            else:
                messages.warning(request, "Insufficient Funds!")
                # return redirect("core:card-detail", credit_card.card_id)
        except (ValueError, InvalidOperation):
            messages.warning(request, "Invalid amount entered!")
        except Exception as e:
            messages.warning(request, f"An error occurred: {str(e)}")
    else:
        messages.warning(request, "An Error Occured, Try again!")
    return redirect("core:card-detail", credit_card.card_id)




def withdraw_fund(request, card_id):
    account = Account.objects.get(user=request.user)
    credit_card = CreditCard.objects.get(card_id=card_id, user=request.user)

    if request.method == "POST":
        amount = request.POST.get("amount")
        print(amount)

        if credit_card.amount >= Decimal(amount) and credit_card.amount != 0.00:
            account.account_balance += Decimal(amount)
            account.save()

            credit_card.amount -= Decimal(amount)
            credit_card.save()

            messages.success(request, "Withdrawal Successfull.")
            return redirect("core:card-detail", credit_card.card_id)
        else:
            messages.warning(request, "Insufficient Funds!")
            return redirect("core:card-detail", credit_card.card_id)




def delete_card(request, card_id):
    credit_card = CreditCard.objects.get(card_id=card_id, user=request.user)
    
    # Before deleting the card, it will be nice to transfer all the money from the card to the main account
    account = request.user.account

    if credit_card.amount > 0:
        account.account_balance += credit_card.amount
        account.save()

        credit_card.delete()
        messages.success(request, "Card deleted Successfully.")
        return redirect("account:dashboard")
    
    credit_card.delete()
    messages.success(request, "Card deleted Successfully.")
    return redirect("account:dashboard")


