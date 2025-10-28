import { TableBody, TableCell, TableRow } from "@/components/ui/table";
import { DraggableRow } from "@/features/DataTables/components/Columns/Components/DragableRow/DragrableRow";
import { PositionsColumns } from "@/features/DataTables/PositionsTable/PositionsColumns/operations/PositionsColumns";
import { type UniqueIdentifier } from "@dnd-kit/core";
import {
  SortableContext,
  verticalListSortingStrategy,
} from "@dnd-kit/sortable";
import type { RowModel } from "@tanstack/react-table";

export interface BodyTableProps {
  tableRowModel: RowModel<any>;
  dataIds: UniqueIdentifier[];
  message: string;
}

export function BodyTable({ tableRowModel, dataIds, message }: BodyTableProps) {
  return (
    <TableBody className="**:data-[slot=table-cell]:first:w-8">
      {tableRowModel.rows?.length ? (
        <SortableContext items={dataIds} strategy={verticalListSortingStrategy}>
          {tableRowModel.rows.map((row) => (
            <DraggableRow key={row.id} row={row} />
          ))}
        </SortableContext>
      ) : (
        <TableRow>
          <TableCell
            colSpan={PositionsColumns.length}
            className="h-24 text-center"
          >
           {message || "No results."}
          </TableCell>
        </TableRow>
      )}
    </TableBody>
  );
}
