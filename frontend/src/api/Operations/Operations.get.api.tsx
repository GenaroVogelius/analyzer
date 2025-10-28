import { getApiUrl } from "@/config/env";
import type { PositionsColumnsType } from "@/features/DataTables/PositionsTable/PositionsColumns/operations/PositionsColumns";
import { useQuery } from "@tanstack/react-query";
import axios from "axios";

export interface OperationsParams {
  from_date: string;
  to_date: string;
  ticker?: string;
  sort?: string;
  offset?: number;
  limit?: number;
}

export interface OperationsResponse {
  message: string;
  data: PositionsColumnsType[];
  pagination: {
    total: number;
    offset: number;
    limit: number;
    has_more: boolean;
  };
}

export const fetchOperations = async (
  params: OperationsParams
): Promise<OperationsResponse> => {
  try {
    const response = await axios.get<OperationsResponse>(
      getApiUrl(`/all-positions`),
      {
        params,
      }
    );

    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      throw new Error(
        `Failed to fetch operations: ${
          error.response?.statusText || error.message
        }`
      );
    }
    throw new Error(`Failed to fetch operations: ${error}`);
  }
};

export const useGetOperations = (params: OperationsParams) => {
  return useQuery({
    queryKey: ["operations", params],
    queryFn: () => fetchOperations(params),
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
