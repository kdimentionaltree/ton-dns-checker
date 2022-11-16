let headers: HeadersInit = {};

if (process.env.REACT_APP_API_KEY)
  headers["X-API-Key"] = process.env.REACT_APP_API_KEY;

export const fetchDHTData = async () => {
  const response = await fetch(
    `${process.env.REACT_APP_API_URL}/api/dns/dhts`,
    {
      headers,
    }
  );
  const data = await response.json();
  return data;
};
export const fetchDHTResolved = async (value: string) => {
  const response = await fetch(
    `${process.env.REACT_APP_API_URL}/api/dns/resolve?adnl=${value}`,
    {
      headers,
    }
  );
  const data = await response.json();
  return data;
};
export const fetchLSData = async () => {
  const response = await fetch(
    `${process.env.REACT_APP_API_URL}/api/dns/liteservers`,
    {
      headers,
    }
  );
  const data = await response.json();
  return data;
};
export const fetchLSResolved = async (value: string) => {
  const response = await fetch(
    `${process.env.REACT_APP_API_URL}/api/dns/ls_resolve?domain=${value}`,
    {
      headers,
    }
  );
  const data = await response.json();
  return data;
};
