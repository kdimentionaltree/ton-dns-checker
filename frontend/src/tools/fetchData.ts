let headers: HeadersInit = {};

const API_URL = process.env.REACT_APP_API_URL ?? "";

if (process.env.REACT_APP_API_KEY)
  headers["X-API-Key"] = process.env.REACT_APP_API_KEY;

export const fetchDHTData = async () => {
  const response = await fetch(
    `${API_URL}/dhts`,
    {
      headers,
    }
  );
  const data = await response.json();
  return data;
};
export const fetchDHTResolved = async (value: string) => {
  const response = await fetch(
    `${API_URL}/resolve?adnl=${value}`,
    {
      headers,
    }
  );
  const data = await response.json();
  return data;
};
export const fetchLSData = async () => {
  const response = await fetch(
    `${API_URL}/liteservers`,
    {
      headers,
    }
  );
  const data = await response.json();
  return data;
};
export const fetchLSResolved = async (value: string) => {
  const response = await fetch(
    `${API_URL}/ls_resolve?domain=${value}`,
    {
      headers,
    }
  );
  const data = await response.json();
  return data;
};
