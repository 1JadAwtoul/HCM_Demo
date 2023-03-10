# Headcount Management Dashboard

### Description:
This project is a web-based dashboard that displays live headcount data for multiple teams, and has the following features:
1. Provides an easy-to-use interface for users to submit headcount shifting requests, which can then be reviewed and approved by team managers.
2. Email notification to all parties involved upon request submission (in the case of this demo, my personal email is used).
3. Allows managers to update the team database with the use of a simple approval button. 

##### `The app has the objective of eliminating extensive manual updates to the database using non-secure mediums as well as improve visibility`

### How do you test this application in your local machine?
1. Clone this repository to your local machine
2. Open your terminal or GitBash
3. Set your directory to the cloned reporsitory in your machine.
4. Activate the virtual environemnt containing all requirements:
```sh
. hc_env/scripts/activate
```
5. Run the application on your local machine:
```sh
streamlit run app2.py
```


```diff
- Please note the email feature will not be functional as of 3/9/23 given that the API key will expire. Hence the reason for not securing. 
```
