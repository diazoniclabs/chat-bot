{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "84abfe57",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Importing necessary libraries\n",
    "import numpy as np\n",
    "from flask import Flask, request, make_response\n",
    "import json\n",
    "import pickle\n",
    "from flask_cors import cross_origin\n",
    "\n",
    "# Declaring the flask app\n",
    "app = Flask(__name__)\n",
    "\n",
    "#Loading the model from pickle file\n",
    "model = pickle.load(open('rf.pkl', 'rb'))\n",
    "\n",
    "\n",
    "# geting and sending response to dialogflow\n",
    "@app.route('/webhook', methods=['POST'])\n",
    "@cross_origin()\n",
    "def webhook():\n",
    "    req = request.get_json(silent=True, force=True)\n",
    "    res = processRequest(req)\n",
    "    res = json.dumps(res, indent=4)\n",
    "    r = make_response(res)\n",
    "    r.headers['Content-Type'] = 'application/json'\n",
    "    return r\n",
    "# processing the request from dialogflow\n",
    "def processRequest(req):\n",
    "\n",
    "\n",
    "    result = req.get(\"queryResult\")\n",
    "    \n",
    "    #Fetching the data points\n",
    "    parameters = result.get(\"parameters\")\n",
    "    Petal_length=parameters.get(\"number\")\n",
    "    Petal_width = parameters.get(\"number1\")\n",
    "    Sepal_length=parameters.get(\"number2\")\n",
    "    Sepal_width=parameters.get(\"number3\")\n",
    "    int_features = [Petal_length,Petal_width,Sepal_length,Sepal_width]\n",
    "    \n",
    "    #Dumping the data into an array\n",
    "    final_features = [np.array(int_features)]\n",
    "    \n",
    "    #Getting the intent which has fullfilment enabled\n",
    "    intent = result.get(\"intent\").get('displayName')\n",
    "    \n",
    "    #Fitting out model with the data points\n",
    "    if (intent=='IrisData'):\n",
    "        prediction = model.predict(final_features)\n",
    "    \n",
    "        output = round(prediction[0], 2)\n",
    "       \t\n",
    "        if(output==0):\n",
    "            flowr = 'Setosa'\n",
    "    \n",
    "        if(output==1):\n",
    "            flowr = 'Versicolour'\n",
    "        \n",
    "        if(output==2):\n",
    "            flowr = 'Virginica'\n",
    "            \n",
    "        #Returning back the fullfilment text back to DialogFlow\n",
    "        fulfillmentText= \"The Iris type seems to be..  {} !\".format(flowr)\n",
    "        #log.write_log(sessionID, \"Bot Says: \"+fulfillmentText)\n",
    "        return {\n",
    "            \"fulfillmentText\": fulfillmentText\n",
    "        }\n",
    "\n",
    "\n",
    "if __name__ == '__main__':\n",
    "    app.run()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "d35f68a2",
   "metadata": {},
   "outputs": [],
   "source": [
    "!Flask --version\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "75a6c72c",
   "metadata": {},
   "outputs": [],
   "source": [
    "numpy._version_"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "ba11f603",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.9.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}