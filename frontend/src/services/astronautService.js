
import api from "./api";

export const getAstronauts = async () => {
  const response = await api.get("/astronauts");
  return response.data;
};

export const getAstronaut = async (astronautId) => {
  const response = await api.get(`/astronauts/${astronautId}`);
  return response.data;
};

export const getAstronautTelemetry = async (astronautId, limit = 100) => {
  const response = await api.get(
    `/astronauts/${astronautId}/telemetry`,
    {
      params: { limit },
    }
  );

  return response.data;
};
