const API_URL = 
http://localhost:5000;

export async function getPatients() {
    const response = await fetch(${API_URL}/patients);
    return response.json();
}
