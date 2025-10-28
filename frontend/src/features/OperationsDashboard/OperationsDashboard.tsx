import { useGetOperations } from "@/api/Operations/Operations.get.api";
import { useUploadOperations } from "@/api/Operations/Operations.post.api";
import { CSVUpload } from "@/components/CSVUpload";
import { DatePicker } from "@/components/DatePicker/DatePicker";
import { PositionsTableSkeleton } from "@/components/PositionsTableSkeleton";
import { Input } from "@/components/ui/input";
import { today, yesterday } from "@/lib/utils";
import { Suspense, useState } from "react";
import { type PositionsColumnsType } from "../DataTables/PositionsTable/PositionsColumns/operations/PositionsColumns";
import { TableContent } from "../TableContent";

export function OperationsDashboard() {
  const [fromDate, setFromDate] = useState<Date | undefined>(yesterday);
  const [toDate, setToDate] = useState<Date | undefined>(today);
  const [ticker, setTicker] = useState<string | undefined>(undefined);
  const [pagination, setPagination] = useState({
    pageIndex: 0,
    pageSize: 10,
  });
  const { data } = useGetOperations({
    from_date: fromDate?.toLocaleDateString() || "",
    to_date: toDate?.toLocaleDateString() || "",
    offset: pagination.pageIndex * pagination.pageSize,
    limit: pagination.pageSize,
    ticker: ticker,
  });

  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  const uploadOperationsMutation = useUploadOperations();



  const handleFileUpload = (file: File) => {
    // Use the TanStack Query mutation to upload the file
    uploadOperationsMutation.mutate(file);
    setSelectedFile(null);
  };

  const handleFileRemove = () => {
    // File removal is handled by the CSVUpload component
  };

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mx-5">
        <div className="flex flex-col gap-4">
          <DatePicker
            label="From Date"
            value={fromDate}
            onChange={setFromDate}
          />
          <DatePicker label="To Date" value={toDate} onChange={setToDate} />
          <Input
            placeholder="Ticket"
            value={ticker}
            onChange={(e) => setTicker(e.target.value)}
            className="w-48"
          />
        </div>
        <div className="flex justify-center md:justify-end">
          <CSVUpload
            selectedFile={selectedFile}
            setSelectedFile={setSelectedFile}
            onFileRemove={handleFileRemove}
            onFileUpload={handleFileUpload}
            maxSize={10}
            className="w-full max-w-sm"
          />
        </div>
      </div>
      <Suspense fallback={<PositionsTableSkeleton />}>
        <TableContent
          data={data?.data as PositionsColumnsType[]}
          pagination={pagination}
          setPagination={setPagination}
          totalRows={data?.pagination.total || 0}
          message={data?.message || ""}
        />
      </Suspense>
    </div>
  );
}
