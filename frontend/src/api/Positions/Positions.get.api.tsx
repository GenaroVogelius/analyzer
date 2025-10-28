import { getApiUrl } from "@/config/env";
import type { PositionsColumnsType } from "@/features/DataTables/PositionsTable/PositionsColumns/closedPositions/closedPositions";
import { useQuery } from "@tanstack/react-query";
import axios from "axios";
export interface PositionsParams {
  from_date: string;
  to_date: string;
  ticker?: string;
  sort?: string;
  offset?: number;
  limit?: number;
}

export interface PositionsResponse {
  message: string;
  data: PositionsColumnsType[];
  pagination: {
    total: number;
    offset: number;
    limit: number;
    has_more: boolean;
  };
}

export const fetchPositions = async (
  params: PositionsParams
): Promise<PositionsResponse> => {
  try {
    const response = await axios.get<PositionsResponse>(
      getApiUrl(`/closed-positions`),
      {
        params,
      }
    );

    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      throw new Error(
        `Failed to fetch review: ${error.response?.statusText || error.message}`
      );
    }
    throw new Error(`Failed to fetch review: ${error}`);
  }
};

export const useGetClosedPositions = (params: PositionsParams) => {
  return useQuery({
    queryKey: ["closed-positions", params],
    queryFn: () => fetchPositions(params),
    staleTime: 5 * 60 * 1000,
    retry: (failureCount, error) => {
      // Don't retry on 404 or 401 errors
      if (error instanceof Error && error.message.includes("404")) {
        return false;
      }
      if (error instanceof Error && error.message.includes("401")) {
        return false;
      }
      return failureCount < 3;
    },
  });
};
