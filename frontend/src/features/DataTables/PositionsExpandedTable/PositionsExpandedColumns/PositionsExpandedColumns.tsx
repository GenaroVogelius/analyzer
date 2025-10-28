import { createColumnHelper } from "@tanstack/react-table";
import { ColumnHeaderSorted } from "../../components/Columns/Components/Columns/ColumnHeaderSorted/ColumnHeaderSorted";

export type PositionsExpandedColumnsType = {
  id: number;
  cantidad_comprada: number;
  precio_compra: number;
  importe_compra: number;
  fecha_compra: string;
  fecha_liquidacion_compra: string;
  fecha_venta: string;
  fecha_liquidacion_venta: string;
  "P&L": number;
  "P&L/d": number;
  "P&L%": number;
  "P&L/d%": number;
  TNA: number;
};

const columnHelper = createColumnHelper<PositionsExpandedColumnsType>();

export const PositionsExpandedColumns = [
  columnHelper.accessor("cantidad_comprada", {
    header: ({ column }) => (
      <ColumnHeaderSorted column={column} title="Cantidad Comprada" />
    ),
    cell: ({ getValue }) => <div className="">{getValue()}</div>,
    sortingFn: "basic",
  }),

  columnHelper.accessor("precio_compra", {
    header: ({ column }) => (
      <ColumnHeaderSorted column={column} title="Precio Compra" />
    ),
    cell: ({ getValue }) => <div className="">{getValue()}</div>,
    sortingFn: "basic",
  }),
  columnHelper.accessor("importe_compra", {
    header: ({ column }) => (
      <ColumnHeaderSorted column={column} title="Importe Compra" />
    ),
    cell: ({ getValue }) => <div className="">{getValue()}</div>,
    sortingFn: "basic",
  }),
  columnHelper.accessor("fecha_compra", {
    header: ({ column }) => (
      <ColumnHeaderSorted column={column} title="Fecha Compra" />
    ),
    cell: ({ getValue }) => <div className="">{getValue()}</div>,
    sortingFn: "basic",
  }),
  columnHelper.accessor("fecha_liquidacion_compra", {
    header: ({ column }) => (
      <ColumnHeaderSorted column={column} title="Fecha Liquidación Compra" />
    ),
    cell: ({ getValue }) => <div className="">{getValue()}</div>,
    sortingFn: "basic",
  }),
  columnHelper.accessor("fecha_venta", {
    header: ({ column }) => (
      <ColumnHeaderSorted column={column} title="Fecha Venta" />
    ),
    cell: ({ getValue }) => <div className="">{getValue()}</div>,
    sortingFn: "basic",
  }),
  columnHelper.accessor("fecha_liquidacion_venta", {
    header: ({ column }) => (
      <ColumnHeaderSorted column={column} title="Fecha Liquidación Venta" />
    ),
    cell: ({ getValue }) => <div className="">{getValue()}</div>,
    sortingFn: "basic",
  }),
  columnHelper.accessor("P&L", {
    header: ({ column }) => (
      <ColumnHeaderSorted
        column={column}
        title="P&L"
        tooltipContent="Profit and losses"
      />
    ),
    cell: ({ getValue }) => <div className="">{getValue()}</div>,
    sortingFn: "basic",
  }),
  columnHelper.accessor("P&L/d", {
    header: ({ column }) => (
      <ColumnHeaderSorted
        column={column}
        title="P&L/d"
        tooltipContent="Profit and losses del dia"
      />
    ),
    cell: ({ getValue }) => <div className="">{getValue()}</div>,
    sortingFn: "basic",
  }),
  columnHelper.accessor("P&L%", {
    header: ({ column }) => (
      <ColumnHeaderSorted
        column={column}
        title="P&L%"
        tooltipContent="Profit and losses percentage"
      />
    ),
    cell: ({ getValue }) => <div className="">{getValue()}</div>,
    sortingFn: "basic",
  }),
  columnHelper.accessor("P&L/d%", {
    header: ({ column }) => (
      <ColumnHeaderSorted
        column={column}
        title="P&L/d%"
        tooltipContent="Profit and losses del dia percentage"
      />
    ),
    cell: ({ getValue }) => <div className="">{getValue()}</div>,
    sortingFn: "basic",
  }),
  columnHelper.accessor("TNA", {
    header: ({ column }) => (
      <ColumnHeaderSorted
        column={column}
        title="TNA"
        tooltipContent="Tasa Nominal Anual"
      />
    ),
    cell: ({ getValue }) => <div className="">{getValue()}</div>,
    sortingFn: "basic",
  }),
];
