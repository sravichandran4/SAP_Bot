'use strict';

const functions = require('firebase-functions');
const admin = require('firebase-admin');
const {WebhookClient} = require('dialogflow-fulfillment');

process.env.DEBUG = 'dialogflow:*'; // enables lib debugging statements
admin.initializeApp(functions.config().firebase);
const db = admin.firestore();

exports.dialogflowFirebaseFulfillment = functions.https.onRequest((request, response) => {
  const agent = new WebhookClient({ request, response });


 function generalInformationHandler (agent) {
    // Get the database collection 'dialogflow' and document 'agent'
   const document = request.body.queryResult.intent.displayName;
    const dialogflowAgentDoc = db.collection('General_information').doc(document);

    // Get the value of 'entry' in the document and send it to the user
    return dialogflowAgentDoc.get()
      .then(doc => {
        if (!doc.exists) {
          agent.add('No data found in the database!');
        } else {
        agent.add(doc.data().A);
        //agent.add('Hey sthis is srudhi');
        }
        return Promise.resolve('Read complete');
      }).catch(() => {
        agent.add('Error reading entry from the Firestore database.');
        agent.add('Please add a entry to the database first by saying, "Write <your phrase> to the database"');
      });

  }

  // Map from Dialogflow intent names to functions to be run when the intent is matched
  let intentMap = new Map();
  const call = request.body.queryResult.intent.displayName;
  intentMap.set(call , generalInformationHandler);
  agent.handleRequest(intentMap);
});
