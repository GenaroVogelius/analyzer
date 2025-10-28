import type {
  ColumnFiltersState,
  SortingState,
  VisibilityState,
} from "@tanstack/react-table";
import {
  getCoreRowModel,
  getExpandedRowModel,
  getFacetedRowModel,
  getFacetedUniqueValues,
  getFilteredRowModel,
  getPaginationRowModel,
  getSortedRowModel,
  useReactTable,
} from "@tanstack/react-table";

import { Table } from "@/components/ui/table";
import { BodyTable } from "@/features/DataTables/components/BodyTable";
import { HeaderTable } from "@/features/DataTables/components/HeaderTable";
import type { PositionsExpandedColumnsType } from "@/features/DataTables/PositionsExpandedTable/PositionsExpandedColumns/PositionsExpandedColumns";
import type { ColumnDef } from "@tanstack/react-table";
import { useState } from "react";

export function PositionsExpandedTable({
  data: initialData,
  columns,
}: {
  data?: PositionsExpandedColumnsType[];
  columns?: ColumnDef<PositionsExpandedColumnsType>[];
}) {
  const [rowSelection, setRowSelection] = useState({});
  const [columnVisibility, setColumnVisibility] = useState<VisibilityState>({});
  const [columnFilters, setColumnFilters] = useState<ColumnFiltersState>([]);
  const [sorting, setSorting] = useState<SortingState>([]);
  const [pagination, setPagination] = useState({
    pageIndex: 0,
    pageSize: 10,
  });

  const table = useReactTable({
    data: initialData || [],
    columns: columns || [],
    state: {
      sorting,
      columnVisibility,
      rowSelection,
      columnFilters,
      pagination,
    },
    enableRowSelection: true,
    onRowSelectionChange: setRowSelection,
    onSortingChange: setSorting,
    onColumnFiltersChange: setColumnFilters,
    onColumnVisibilityChange: setColumnVisibility,
    onPaginationChange: setPagination,
    getCoreRowModel: getCoreRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getExpandedRowModel: getExpandedRowModel(),
    getFacetedRowModel: getFacetedRowModel(),
    getFacetedUniqueValues: getFacetedUniqueValues(),
  });

  return (
    <div className="w-full flex flex-col justify-start gap-6">
      <div className="relative flex flex-col gap-4 overflow-auto pl-6 py-2 pr-2">
        <div className="overflow-hidden rounded-lg border">
          <Table>
            <HeaderTable tableHeaderGroups={table.getHeaderGroups()} />
            <BodyTable
              tableRowModel={table.getRowModel()}
              dataIds={initialData?.map(({ id }) => id) || []}
            />
          </Table>
        </div>
      </div>
    </div>
  );
}
