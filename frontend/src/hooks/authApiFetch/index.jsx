import { useState, useEffect } from 'react';
async function useAuthFetch(url, options = {}) {
    options.credentials = 'include'
    options.headers['Content-Type'] = 'application/json'

    async function callRefreshEndpoint() {
        const refresh_response = await fetch(
            `${import.meta.env.VITE_SERVER_URL}\\auth\\jwt\\refresh\\`, {method: 'POST', credentials: 'include'})
        if (refresh_response.status == 200){
                return true
            }
        return false
    }
    async function callEndpoint(calledRefresh=false) {
        const response = await fetch(url, options)
        if (!calledRefresh && response.status == 401 && await callRefreshEndpoint()){
            callEndpoint(true)
        }
        else if (response.status == 401){
            return [null, await response.json()]
            }
        return [await response.json(), null]
    }
    return callEndpoint()

}
export default useAuthFetch;