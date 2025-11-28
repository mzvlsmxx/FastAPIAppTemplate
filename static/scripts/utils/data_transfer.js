export async function fetchData() {
    const params = new URLSearchParams(
        {
            "query_parameter_1": "some_value",
            "query_parameter_2": "another_value"
        }
    );
    const response = await fetch(
        `/data/fetch?${params.toString()}`,
        {
            method: "GET",
            headers: {
                "Content-Type": "application/json"
            }
        }
    );
    return response;
}


export async function sendData(data) {
    const params = new URLSearchParams(
        {
            "query_parameter_1": "some_value",
            "query_parameter_2": "another_value"
        }
    )
    const response = await fetch(
        `/data/process?${params.toString()}`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        }
    );
    return response;
}