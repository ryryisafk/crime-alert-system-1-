import axios from "axios";

const API_BASE = "http://127.0.0.1:8000";

export const getDashboardSummary = () =>
  axios.get(`${API_BASE}/dashboard/summary`).then((res) => res.data);

export const getCrimeByDistrict = () =>
  axios.get(`${API_BASE}/dashboard/crime-by-district`).then((res) => res.data);

export const getMonthlyTrend = () =>
  axios.get(`${API_BASE}/dashboard/monthly-trend`).then((res) => res.data);

export const getHotspots = () =>
  axios.get(`${API_BASE}/hotspots/`).then((res) => res.data);

export const getAlerts = () =>
  axios.get(`${API_BASE}/alerts/`).then((res) => res.data);

export const getCrimes = () =>
  axios.get(`${API_BASE}/crimes/`).then((res) => res.data);

export const predictCrime = (data) =>
  axios
    .post(`${API_BASE}/predict/`, data)
    .then((res) => res.data);

export const getDistricts = () =>
  axios.get(`${API_BASE}/predict/districts`).then(res => res.data);

export const getCrimeTypes = () =>
  axios.get(`${API_BASE}/predict/crime-types`).then(res => res.data);