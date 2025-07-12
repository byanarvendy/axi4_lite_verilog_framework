import sys
import os


def parse_args(arg):
    if not arg.startswith("m") or "s" not in arg:
        raise ValueError("Format must be 'm{n}s{n}', example: m2s1")
    m_part, s_part = arg[1:].split("s")
    return int(m_part), int(s_part)


def gen_module(m, s):
    code = []

    # module header
    code.append(f"module axi4_lite_interconnect_m{m}s{s} #(")

    # parameters
    code.append(f"    /* parameters */")
    code.append("    parameter ADDR_WIDTH    = 32,")
    code.append("    parameter DATA_WIDTH    = 32,")
    code.append("")

    # generate address parameters for each slave
    code.append(f"    /* address parameters */")
    for i in range(s):
        code.append(f"    parameter LOW_ADDR{i}     = 32'h{i:04x}_0000,")
        code.append(
            f"    parameter HIGH_ADDR{i}    = 32'h{i:04x}_FFFF{',' if i != s-1 else ''}"
        )

    code.append(") (")
    code.append("    input                               iCLK, iRST,")
    code.append("")

    # master interfaces
    for master in range(m):
        code.append(f"    /* master interface {master} */")
        code.append("        /* write address channel */    ")
        code.append(f"        input                           m{master}_AWVALID,")
        code.append(f"        input   [ADDR_WIDTH-1:0]        m{master}_AWADDR,")
        code.append(f"        output                          m{master}_AWREADY,")
        code.append("")
        code.append("        /* write data channel */    ")
        code.append(f"        input                           m{master}_WVALID,")
        code.append(f"        input   [(DATA_WIDTH/8)-1:0]    m{master}_WSTRB,")
        code.append(f"        input   [DATA_WIDTH-1:0]        m{master}_WDATA,")
        code.append(f"        output                          m{master}_WREADY,")
        code.append("")
        code.append("        /* write response channel */    ")
        code.append(f"        input                           m{master}_BREADY,")
        code.append(f"        output                          m{master}_BVALID,")
        code.append(f"        output  [1:0]                   m{master}_BRESP,")
        code.append("")
        code.append("        /* read address channel */    ")
        code.append(f"        input                           m{master}_ARVALID,")
        code.append(f"        input   [DATA_WIDTH-1:0]        m{master}_ARADDR,")
        code.append(f"        output                          m{master}_ARREADY,")
        code.append("")
        code.append("        /* read data channel */    ")
        code.append(f"        input                           m{master}_RREADY,")
        code.append(f"        output                          m{master}_RVALID,")
        code.append(f"        output  [1:0]                   m{master}_RRESP,")
        code.append(
            f"        output  [DATA_WIDTH-1:0]        m{master}_RDATA{',' if master != m-1 or s > 0 else ''}"
        )
        code.append("")

    # slave interfaces
    for slave in range(s):
        code.append(f"    /* slave interface {slave} */")
        code.append("        /* write address channel */")
        code.append(f"        input                           s{slave}_AWREADY,")
        code.append(f"        output                          s{slave}_AWVALID,")
        code.append(f"        output  [ADDR_WIDTH-1:0]        s{slave}_AWADDR,")
        code.append("")
        code.append("        /* write data channel */")
        code.append(f"        input                           s{slave}_WREADY,")
        code.append(f"        output                          s{slave}_WVALID,")
        code.append(f"        output  [(DATA_WIDTH/8)-1:0]    s{slave}_WSTRB,")
        code.append(f"        output  [DATA_WIDTH-1:0]        s{slave}_WDATA,")
        code.append("")
        code.append("        /* write response channel */")
        code.append(f"        input                           s{slave}_BVALID,")
        code.append(f"        input   [1:0]                   s{slave}_BRESP,")
        code.append(f"        output                          s{slave}_BREADY,")
        code.append("")
        code.append("        /* read address channel */")
        code.append(f"        input                           s{slave}_ARREADY,")
        code.append(f"        output                          s{slave}_ARVALID,")
        code.append(f"        output  [ADDR_WIDTH-1:0]        s{slave}_ARADDR,")
        code.append("")
        code.append("        /* read data channel */")
        code.append(f"        input                           s{slave}_RVALID,")
        code.append(f"        input   [1:0]                   s{slave}_RRESP,")
        code.append(f"        input   [DATA_WIDTH-1:0]        s{slave}_RDATA,")
        code.append(
            f"        output                          s{slave}_RREADY{',' if slave != s - 1 else ''}"
            + ("" if slave == s - 1 else "\n")
        )

    code.append(");")
    code.append("")

    # finite state machine
    code.append("    /* finite state machine */")
    code.append("    localparam IDLE     = 3'b000;")
    code.append("    localparam WRITE    = 3'b001;")
    code.append("    localparam READ     = 3'b010;")
    code.append("")
    code.append("    reg         read_start, write_start;")
    code.append(f"    reg [{max(1, (m-1).bit_length())}:0]   sel_m;")
    code.append(f"    reg [{max(1, (s-1).bit_length())}:0]   sel_s;")
    code.append(f"    reg [{max(1, (s-1).bit_length())}:0]   sel_s_reg;")
    code.append(f"    reg [{max(1, (m-1).bit_length())}:0]   sel_m_reg;")
    code.append("    reg [2:0]   state, next_state;")
    code.append("")
    code.append("    initial begin")
    code.append(f"        sel_s       = {s};")
    code.append(f"        sel_m       = {m};")
    code.append("    end")
    code.append("")
    code.append("    always @(posedge iCLK or negedge iRST) begin")
    code.append("        if (!iRST) begin")
    code.append("            state           <= IDLE;")
    code.append(f"            sel_s_reg       <= {s};")
    code.append(f"            sel_m_reg       <= {m};")
    code.append("        end else begin")
    code.append("            state           <= next_state;")
    code.append("            if (state == IDLE) begin")
    code.append("                sel_s_reg   <= sel_s;")
    code.append("                sel_m_reg   <= sel_m;")
    code.append("            end")
    code.append("        end")
    code.append("    end")
    code.append("")
    code.append("    always @(*) begin")
    code.append("        case (state)")
    code.append(
        "            IDLE: next_state = (write_start) ? WRITE : ((read_start) ? READ : IDLE);"
    )
    code.append("            WRITE: begin")
    code.append("                case(sel_s)")
    for slave in range(s):
        for master in range(m):
            code.append(
                f"                    {slave}: next_state = (s{slave}_BVALID && m{master}_BREADY) ? IDLE : WRITE;"
            )
    code.append("                    default: next_state = WRITE;")
    code.append("                endcase")
    code.append("            end")
    code.append("            READ : begin")
    code.append("                case(sel_s)")
    for slave in range(s):
        for master in range(m):
            code.append(
                f"                    {slave}: next_state = (s{slave}_RVALID && m{master}_RREADY) ? IDLE : READ;"
            )
    code.append("                    default: next_state = READ;")
    code.append("                endcase")
    code.append("            end")
    code.append("            default: next_state = IDLE;")
    code.append("        endcase")
    code.append("    end")
    code.append("")
    code.append("    always @(*) begin")
    code.append("        read_start  = 0;")
    code.append("        write_start = 0;")
    code.append("        if (state == IDLE) begin")
    for master in range(m):
        code.append(f"            if (m{master}_ARVALID) begin ")
        code.append(
            f"                sel_m = {master}; write_start = 0; read_start = 1;"
        )
        code.append(f"            end else if (m{master}_AWVALID) begin")
        code.append(
            f"                sel_m = {master}; write_start = 1; read_start = 0;"
        )
        code.append("            end")
    code.append(f"            else sel_m = {m};")
    code.append("        end else sel_m = sel_m_reg;")
    code.append("    end")
    code.append("")
    code.append("    always @(*) begin")
    code.append("        if (state == IDLE) begin")
    code.append("            if (write_start) begin")
    code.append("                case (sel_m)")
    for master in range(m):
        code.append(f"                    {master}: begin")
        for slave in range(s):
            if slave == 0:
                code.append(
                    f"                        if      (m{master}_AWADDR >= LOW_ADDR{slave} && m{master}_AWADDR <= HIGH_ADDR{slave}) sel_s = {slave};"
                )
            else:
                code.append(
                    f"                        else if (m{master}_AWADDR >= LOW_ADDR{slave} && m{master}_AWADDR <= HIGH_ADDR{slave}) sel_s = {slave};"
                )
        code.append(f"                        else    sel_s = {s};")
        code.append("                    end")
    code.append(f"                    default: sel_s = {s};")
    code.append("                endcase")
    code.append("            end")
    code.append("            else if (read_start) begin")
    code.append("                case (sel_m)")
    for master in range(m):
        code.append(f"                    {master}: begin")
        for slave in range(s):
            if slave == 0:
                code.append(
                    f"                        if      (m{master}_ARADDR >= LOW_ADDR{slave} && m{master}_ARADDR <= HIGH_ADDR{slave}) sel_s = {slave};"
                )
            else:
                code.append(
                    f"                        else if (m{master}_ARADDR >= LOW_ADDR{slave} && m{master}_ARADDR <= HIGH_ADDR{slave}) sel_s = {slave};"
                )
        code.append(f"                        else    sel_s = {s};")
        code.append("                    end")
    code.append(f"                    default: sel_s = {s};")
    code.append("                endcase")
    code.append(f"            end else sel_s = {s};")
    code.append("        end else  sel_s = sel_s_reg;")
    code.append("    end")
    code.append("")

    # master connections
    for master in range(m):
        code.append(f"    /* master {master} */")
        code.append("        /* write */")
        awready_parts = [
            f"(sel_s_reg == {slave}) ? s{slave}_AWREADY" for slave in range(s)
        ]
        code.append(
            f"        assign m{master}_AWREADY   = {' : '.join(awready_parts)} : 1'b0;"
        )
        wready_parts = [
            f"(sel_s_reg == {slave}) ? s{slave}_WREADY" for slave in range(s)
        ]
        code.append(
            f"        assign m{master}_WREADY    = {'  : '.join(wready_parts)}  : 1'b0;"
        )
        bresp_parts = [f"(sel_s_reg == {slave}) ? s{slave}_BRESP" for slave in range(s)]
        code.append(
            f"        assign m{master}_BRESP     = {'   : '.join(bresp_parts)}   : 2'b00;"
        )
        bvalid_parts = [
            f"(sel_s_reg == {slave}) ? s{slave}_BVALID" for slave in range(s)
        ]
        code.append(
            f"        assign m{master}_BVALID    = {'  : '.join(bvalid_parts)}  : 1'b0;"
        )
        code.append("")

        code.append("        /* read */")
        arready_parts = [
            f"(sel_s_reg == {slave}) ? s{slave}_ARREADY" for slave in range(s)
        ]
        code.append(
            f"        assign m{master}_ARREADY   = {' : '.join(arready_parts)} : 1'b0;"
        )
        rvalid_parts = [
            f"(sel_s_reg == {slave}) ? s{slave}_RVALID" for slave in range(s)
        ]
        code.append(
            f"        assign m{master}_RVALID    = {'  : '.join(rvalid_parts)}  : 1'b0;"
        )
        rdata_parts = [f"(sel_s_reg == {slave}) ? s{slave}_RDATA" for slave in range(s)]
        code.append(
            f"        assign m{master}_RDATA     = {'   : '.join(rdata_parts)}   : 32'h0;"
        )
        rresp_parts = [f"(sel_s_reg == {slave}) ? s{slave}_RRESP" for slave in range(s)]
        code.append(
            f"        assign m{master}_RRESP     = {'   : '.join(rresp_parts)}   : 2'b00;"
        )
        code.append("")

    # slave connections
    for slave in range(s):
        code.append(f"    /* slave {slave} */")
        code.append("        /* write */")
        for master in range(m):
            code.append(
                f"        assign s{slave}_AWADDR   = ((sel_s_reg == {slave}) && m{master}_AWVALID && (sel_m_reg == {master})) ? m{master}_AWADDR - LOW_ADDR{slave}   : 32'h0;"
            )
            code.append(
                f"        assign s{slave}_AWVALID  = ((sel_s_reg == {slave}) && m{master}_AWVALID && (sel_m_reg == {master})) ? m{master}_AWVALID              : 1'b0;"
            )

            code.append(
                f"        assign s{slave}_WVALID   = ((sel_s_reg == {slave}) && m{master}_WVALID  && (sel_m_reg == {master})) ? m{master}_WVALID               : 1'b0;"
            )
            code.append(
                f"        assign s{slave}_WDATA    = ((sel_s_reg == {slave}) && m{master}_WDATA   && (sel_m_reg == {master})) ? m{master}_WDATA                : 32'h0;"
            )
            code.append(
                f"        assign s{slave}_WSTRB    = ((sel_s_reg == {slave}) && m{master}_WSTRB   && (sel_m_reg == {master})) ? m{master}_WSTRB                : 4'h0;"
            )
            code.append(
                f"        assign s{slave}_BREADY   = ((sel_s_reg == {slave}) && m{master}_BREADY  && (sel_m_reg == {master})) ? m{master}_BREADY               : 1'b0;"
            )
            code.append("")
        code.append("        /* read */")
        for master in range(m):
            code.append(
                f"        assign s{slave}_ARADDR   = ((sel_s_reg == {slave}) && m{master}_ARVALID && (sel_m_reg == {master})) ? m{master}_ARADDR - LOW_ADDR{slave}   : 32'h0;"
            )
            code.append(
                f"        assign s{slave}_ARVALID  = ((sel_s_reg == {slave}) && m{master}_ARVALID && (sel_m_reg == {master})) ? m{master}_ARVALID              : 1'b0;"
            )

            code.append(
                f"        assign s{slave}_RREADY   = ((sel_s_reg == {slave}) && m{master}_RREADY  && (sel_m_reg == {master})) ? m{master}_RREADY               : 1'b0;"
            )
            code.append("")

    code.append("endmodule")

    return "\n".join(code)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python generator.py mXsY (e.g., m2s2)")
        sys.exit(1)

    try:
        m, s = parse_args(sys.argv[1])
        verilog_code = gen_module(m, s)
        output_dir = "logical/rtl/axi4_lite_interconnect"
        os.makedirs(output_dir, exist_ok=True)

        filename = f"{output_dir}/axi4_lite_interconnect_m{m}s{s}.v"
        with open(filename, "w") as f:
            f.write(verilog_code)
        print(f"Generated: {filename}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
