import { useGetClosedPositions } from "@/api/Positions/Positions.get.api";
import { DatePicker } from "@/components/DatePicker/DatePicker";
import { PositionsTableSkeleton } from "@/components/PositionsTableSkeleton";
import { Input } from "@/components/ui/input";
import { today, yesterday } from "@/lib/utils";
import type { ColumnDef } from "@tanstack/react-table";
import { Suspense, useState } from "react";
import {
  PositionsColumns,
  type PositionsColumnsType,
} from "../DataTables/PositionsTable/PositionsColumns/closedPositions/closedPositions";
import { PositionsTable } from "../DataTables/PositionsTable/PositionsTable";

export function ClosedPositionsDashboard() {
  const [fromDate, setFromDate] = useState<Date | undefined>(yesterday);
  const [toDate, setToDate] = useState<Date | undefined>(today);
  const [ticker, setTicker] = useState<string | undefined>(undefined);
  const [pagination, setPagination] = useState({
    pageIndex: 0,
    pageSize: 10,
  });
  const { data, isLoading, error } = useGetClosedPositions({
    from_date: fromDate?.toLocaleDateString() || "",
    to_date: toDate?.toLocaleDateString() || "",
    offset: pagination.pageIndex * pagination.pageSize,
    limit: pagination.pageSize,
    ticker: ticker || undefined,
  });

  console.log(data);
  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-4">
        <DatePicker label="From Date" value={fromDate} onChange={setFromDate} />
        <DatePicker label="To Date" value={toDate} onChange={setToDate} />
        <Input
          placeholder="Ticket"
          value={ticker}
          onChange={(e) => setTicker(e.target.value)}
        />
      </div>
      <Suspense fallback={<PositionsTableSkeleton />}>
        <PositionsTable
          data={data?.data as PositionsColumnsType[]}
          columns={PositionsColumns as ColumnDef<PositionsColumnsType>[]}
          pagination={pagination}
          onPaginationChange={setPagination}
          totalRows={data?.pagination.total || 0}
          manualPagination={true}
          hasDeleteButton={false}
          message={data?.message || ""}
        />
      </Suspense>
    </div>
  );
}
