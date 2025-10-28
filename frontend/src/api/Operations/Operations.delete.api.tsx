import { getApiUrl } from "@/config/env";
import type { PositionsColumnsType } from "@/features/DataTables/PositionsTable/PositionsColumns/operations/PositionsColumns";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import axios from "axios";
import { toast } from "sonner";

export interface OperationsParams {
  ids: number[];
}

export interface DeleteOperationsResponse {
  message: string;
  data: PositionsColumnsType[];
  pagination: {
    total: number;
    offset: number;
    limit: number;
    has_more: boolean;
  };
}

export const deleteOperations = async (
  ids: number[]
): Promise<DeleteOperationsResponse> => {
  try {
    const response = await axios.delete<DeleteOperationsResponse>(
      getApiUrl(`/delete-positions`),
      {
        data: {
          ids: ids,
        },
      }
    );

    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      throw new Error(
        `Failed to delete operations: ${
          error.response?.statusText || error.message
        }`
      );
    }
    throw new Error(`Failed to delete operations: ${error}`);
  }
};

export const useDeleteOperations = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (ids: number[]) => deleteOperations(ids),
    onSuccess: (_, ids) => {
      // Invalidate operations query to trigger refetch
      queryClient.invalidateQueries({ queryKey: ["operations"] });

      // Show success toast
      toast.success(
        `Successfully deleted ${ids.length} operation${
          ids.length > 1 ? "s" : ""
        }`
      );
    },
    onError: (error) => {
      // Show error toast
      const errorMessage =
        error instanceof Error ? error.message : "Failed to delete operations";
      toast.error(`Delete failed: ${errorMessage}`);
    },
  });
};
