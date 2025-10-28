import { getApiUrl } from "@/config/env";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import axios from "axios";
import { toast } from "sonner";

export interface UploadOperationsResponse {
  message: string;
  status: "success" | "error";
}

export const uploadOperations = async (
  file: File
): Promise<UploadOperationsResponse> => {
  try {
    const formData = new FormData();
    formData.append("file", file);

    const response = await axios.post<UploadOperationsResponse>(
      getApiUrl("/upload-operations"),
      formData,
      {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      }
    );

    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      throw new Error(
        `Failed to upload operations: ${
          error.response?.statusText || error.message
        }`
      );
    }
    throw new Error(`Failed to upload operations: ${error}`);
  }
};

export const useUploadOperations = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (file: File) => uploadOperations(file),
    onSuccess: (data) => {
      // Invalidate operations query to trigger refetch
      queryClient.invalidateQueries({ queryKey: ["operations"] });

      // Show success toast with the message from the API
      if (data.status === "success") {
        toast.success(data.message);
      } else {
        toast.error(data.message);
      }
    },
    onError: (error) => {
      // Show error toast
      const errorMessage =
        error instanceof Error ? error.message : "Failed to upload operations";
      toast.error(`Upload failed: ${errorMessage}`);
    },
  });
};
