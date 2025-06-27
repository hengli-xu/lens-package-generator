#FROM python:3.7
#
#WORKDIR /app
#
#ADD requirements.txt ./requirements.txt
#ADD ./Cash_Incentive_API_Automation Cash_Incentive_API_Automation
#RUN pip3 install -r requirements.txt
##RUN pip3 install ptest
##RUN apt-get update -y
##RUN apt-get install -y freetds-dev gcc curl vim
#
#CMD ["/usr/local/bin/ptest3","-t", "Cash_Incentive_API_Automation.test.ads_billing.BillingServiceTest.BillingServiceTest"]


FROM python

WORKDIR /app

ADD requirements.txt ./requirements.txt
ADD api_business ./api_business
ADD common_libs ./common_libs
ADD settings ./settings
ADD test ./test
ADD test_data ./test_data
ADD test_output ./test_output

#ADD ./Cash_Incentive_API_Automation Cash_Incentive_API_Automation
# prepare environment
RUN pip3 install -r requirements.txt
#RUN pip3 install ptest
#RUN apt-get update -y
#RUN apt-get install -y freetds-dev gcc curl vim
#CMD ["pytest", "test/test_temp.py"]
#CMD ["/usr/local/bin/ptest3","-t", "Cash_Incentive_API_Automation.test.ads_billing.BillingServiceTest.BillingServiceTest"]
#CMD ["pytest", "test/test_cash_iq_insights/test_insights_sales_by_state.py"]
CMD ["pytest", "test/test_cash_iq_insights/test_insights_sales_by_state.py", "--html=1.html"]
CMD ["/bin/bash"]