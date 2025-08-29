import random
from agents import function_tool
from pydantic import BaseModel


class ServiceType(BaseModel):
   service: str
   confidence : float
   keywords_detected: list[str]
   reasoning : str
   


class ToolInfo(BaseModel):
   token_number: str 
   wait_time: str 
   message: str
   service_type: str
   
#-----------------------------------------------
@function_tool
def identify_banking_purpose(customer_request: str):
   """it is a simple function to figure out what banking service customer needs."""
    
   request = customer_request.lower()
 
   if ("balance" in request) or ("account" in request) or ("statement" in request)  :
      return ServiceType(
         service = "account_service",
         confidence = 0.9,
         keywords_detected = ["balance","account","statement"],
         reasoning = "Customer want to check their account"
      )
      
   elif ("transfer" in request) or ("send" in request) or ("payment" in request)  :
      return ServiceType(
         service = "transfer_service",
         confidence = 0.9,
         keywords_detected = ["transfer","send","payment"],
         reasoning = "Customer want to send money or make payment"
      )
   elif ("loan" in request) or ("mortgage" in request) or ("borrow" in request)  :
      return ServiceType(
         service = "loan_service",
         confidence = 0.9,
         keywords_detected = ["loan","mortgage","borrow"],
         reasoning = "Customer need help with loan."
      )
   else:
       return ServiceType(
         service = "general_banking",
         confidence = 0.5,
         keywords_detected = ["general"],
         reasoning = "Customer needs general banking help."
      )
      

@function_tool
def generate_customer_token(service_type: str = "general")-> ToolInfo:
    """"Generates a token number for the customer queue.the value of service_type argument can be only these as mention below 
    
     Args: service_type = "general" , service_type = "account_service" , service_type = "transfer_service"  ,
       service_type = "loan_service"
       """
  
    if service_type == "account_service":
       prefix= "A"
       waite_time = "5-10 minutes"
    elif service_type == "transfer_service":
       prefix= "T"
       waite_time = "2-5 minutes"
    elif service_type == "loan_service":
       prefix= "L"
       waite_time = "15-20 minutes"
    else:
       prefix= "G"
       waite_time = "8-10 minutes"
    token_number = f"{prefix}{random.randint(100, 9999)}"   

    return ToolInfo(
        token_number=token_number,
        wait_time=waite_time,
        message=f"please take token  {token_number} and wait for a {waite_time}, and have a seat, we will call you shortly!",
        service_type=service_type
    )