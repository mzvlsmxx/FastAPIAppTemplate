import * as dom from './dom_elements.js';
import * as dataTransfer from './utils/data_transfer.js';


dom.exampleBtn.addEventListener("click", test);


async function test() {
    const dataToSend = {
        someData: "Some data to process"
    };
    await dataTransfer.sendData(dataToSend).then(
        sendDataResponse => {
            console.log(
                {
                    "sendDataStatus": sendDataResponse.status,
                    "sendDataJSON": sendDataResponse.json()
                }
            );
        }
    );
    await dataTransfer.fetchData().then(
        fetchDataResponse => {
            console.log(
                {
                    "fetchDataStatus": fetchDataResponse.status,
                    "fetchDataJSON": fetchDataResponse.json()
                }
            );
        }
    );
}
