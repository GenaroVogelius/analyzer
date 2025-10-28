import {
  KeyboardSensor,
  MouseSensor,
  TouchSensor,
  useSensor,
  useSensors,
  type DragEndEvent,
  type UniqueIdentifier,
} from "@dnd-kit/core";
import { arrayMove } from "@dnd-kit/sortable";
import type {
  ColumnFiltersState,
  ExpandedState,
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

import { ColumnsOptions } from "@/components/ColumnsOptions";
import { Table } from "@/components/ui/table";
import type { ColumnDef } from "@tanstack/react-table";
import { useEffect, useId, useMemo, useState } from "react";
import { BodyTable } from "../components/BodyTable";
import { DragAndDropProvider } from "../components/DragAndDropProvider";
import { FooterTable } from "../components/FooterTable";
import { HeaderTable } from "../components/HeaderTable";

export function PositionsTable<T extends { id: number }>({
  data: initialData,
  columns,
  pagination: externalPagination,
  onPaginationChange,
  totalRows,
  manualPagination = false,
  hasDeleteButton = false,
  message,
}: {
  data?: T[];
  columns?: ColumnDef<T>[];
  pagination?: { pageIndex: number; pageSize: number };
  onPaginationChange?: (pagination: {
    pageIndex: number;
    pageSize: number;
  }) => void;
  totalRows?: number;
  manualPagination?: boolean;
  hasDeleteButton?: boolean;
  message: string;
}) {
  const [data, setData] = useState(() => initialData);
  const [rowSelection, setRowSelection] = useState({});
  const [columnVisibility, setColumnVisibility] = useState<VisibilityState>({});
  const [columnFilters, setColumnFilters] = useState<ColumnFiltersState>([]);
  const [sorting, setSorting] = useState<SortingState>([]);
  const [internalPagination, setInternalPagination] = useState({
    pageIndex: 0,
    pageSize: 10,
  });
  const [expanded, setExpanded] = useState<ExpandedState>({});

  // Update data when initialData prop changes (for server-side pagination)
  useEffect(() => {
    setData(initialData);
  }, [initialData]);

  // Use external pagination if manualPagination is true, otherwise use internal
  const pagination = manualPagination
    ? externalPagination || { pageIndex: 0, pageSize: 10 }
    : internalPagination;

  const handlePaginationChange = (updaterOrValue: any) => {
    if (manualPagination && onPaginationChange) {
      const newPagination =
        typeof updaterOrValue === "function"
          ? updaterOrValue(pagination)
          : updaterOrValue;
      onPaginationChange(newPagination);
    } else {
      setInternalPagination(updaterOrValue);
    }
  };
  const sortableId = useId();
  const sensors = useSensors(
    useSensor(MouseSensor, {}),
    useSensor(TouchSensor, {}),
    useSensor(KeyboardSensor, {})
  );

  const dataIds = useMemo<UniqueIdentifier[]>(
    () => data?.map(({ id }) => id) || [],
    [data]
  );

  const table = useReactTable({
    data: data || [],
    columns: columns || [],
    state: {
      sorting,
      columnVisibility,
      rowSelection,
      columnFilters,
      pagination,
      expanded,
    },
    getRowId: (row) => row.id.toString(),
    enableRowSelection: true,
    enableExpanding: true,
    manualPagination: manualPagination,
    pageCount:
      manualPagination && totalRows
        ? Math.ceil(totalRows / pagination.pageSize)
        : undefined,
    onRowSelectionChange: setRowSelection,
    onSortingChange: setSorting,
    onColumnFiltersChange: setColumnFilters,
    onColumnVisibilityChange: setColumnVisibility,
    onPaginationChange: handlePaginationChange,
    onExpandedChange: setExpanded,
    getCoreRowModel: getCoreRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
    getPaginationRowModel: manualPagination
      ? undefined
      : getPaginationRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getExpandedRowModel: getExpandedRowModel(),
    getFacetedRowModel: getFacetedRowModel(),
    getFacetedUniqueValues: getFacetedUniqueValues(),
  });

  function handleDragEnd(event: DragEndEvent) {
    const { active, over } = event;
    if (active && over && active.id !== over.id) {
      setData((data) => {
        const oldIndex = dataIds.indexOf(active.id);
        const newIndex = dataIds.indexOf(over.id);
        return arrayMove(data || [], oldIndex, newIndex);
      });
    }
  }

  return (
    <div className="w-full flex flex-col justify-start gap-6">
      <ColumnsOptions columns={table.getAllColumns()} />
      <div className="relative flex flex-col gap-4 overflow-auto px-4">
        <div className="overflow-hidden rounded-lg border">
          <DragAndDropProvider
            handleDragEnd={handleDragEnd}
            sensors={sensors}
            sortableId={sortableId}
          >
            <Table>
              <HeaderTable tableHeaderGroups={table.getHeaderGroups()} />
              <BodyTable
                tableRowModel={table.getRowModel()}
                dataIds={dataIds}
                message={message}
              />
            </Table>
          </DragAndDropProvider>
        </div>
        <FooterTable table={table} hasDeleteButton={hasDeleteButton} />
      </div>
    </div>
  );
}
