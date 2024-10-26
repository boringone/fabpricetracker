import { useState, useEffect } from 'react';
function useAuthFetch(url, options) {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  useEffect(() => {
    fetch(url, options)
      .then(response => response.json())
      .then(data => {
        setData(data);
      })
      .catch(error => {
        setError(error);
      });
  }, [url, options]);
  return { data, error };
}
export default useFetch;