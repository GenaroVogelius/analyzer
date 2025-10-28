import type { ColumnDef } from "@tanstack/react-table";
import {
  PositionsColumns,
  type PositionsColumnsType,
} from "../DataTables/PositionsTable/PositionsColumns/operations/PositionsColumns";
import { PositionsTable } from "../DataTables/PositionsTable/PositionsTable";

export function TableContent({
  data,
  pagination,
  setPagination,
  totalRows,
  message,
}: {
  data: PositionsColumnsType[];
  pagination: { pageIndex: number; pageSize: number };
  setPagination: (pagination: { pageIndex: number; pageSize: number }) => void;
  totalRows: number;
  message: string;
}) {
  const handlePaginationChange = (newPagination: {
    pageIndex: number;
    pageSize: number;
  }) => {
    setPagination(newPagination);
  };

  return (
    <PositionsTable
      data={data as PositionsColumnsType[]}
      columns={PositionsColumns as ColumnDef<PositionsColumnsType>[]}
      pagination={pagination}
      onPaginationChange={handlePaginationChange}
      totalRows={totalRows}
      manualPagination={true}
      hasDeleteButton={true}
      message={message}
    />
  );
}
