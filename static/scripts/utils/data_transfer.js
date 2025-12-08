async function getOnAPI(url, urlParams) {
    const params = new URLSearchParams(urlParams);
    const response = await fetch(
        `${url}?${params.toString()}`,
        {
            method: "GET",
            headers: {"Content-Type": "application/json"}
        }
    );
    return response;
}


async function postOnAPI(url, urlParams, body) {
    const params = new URLSearchParams(urlParams);
    const response = await fetch(
        `${url}?${params.toString()}`,
        {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(body)
        }
    );
    return response;
}


export async function fetchData() {
    const apiResponse = await getOnAPI(
        '/data/fetch',
        {
            "query_parameter_1": "some_value",
            "query_parameter_2": "another_value"
        }
    );
    return apiResponse;
}


export async function sendData(data) {
    const apiResponse = await postOnAPI(
        '/data/process',
        {
            "query_parameter_1": "some_value",
            "query_parameter_2": "another_value"
        },
        data
    );
    return apiResponse;
}