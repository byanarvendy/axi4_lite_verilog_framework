`timescale 1ns / 1ns

module tb_axi4_lite_interconnect_m1s2();
    /* address parameters */
    parameter LOW_ADDR0     = 32'h00000000;
    parameter HIGH_ADDR0    = 32'h000000ff;
    parameter LOW_ADDR1     = 32'h00000100;
    parameter HIGH_ADDR1    = 32'h000001ff;

    parameter           CLK_PERIOD = 10;
    reg                 iCLK, iRST;

    /* master 0 interfaces */
    reg                 m0_write_req;
    reg     [3:0]       m0_write_strb;
    reg     [31:0]      m0_write_addr, m0_write_data;
    wire    [1:0]       m0_write_resp;
    
    reg                 m0_read_req;
    reg     [31:0]      m0_read_addr;
    wire    [1:0]       m0_read_resp;
    wire    [31:0]      m0_read_data;
    
    
    /* master 0 signals */
    wire                m0_AWVALID, m0_AWREADY;
    wire    [31:0]      m0_AWADDR;
    
    wire                m0_WVALID, m0_WREADY;
    wire    [3:0]       m0_WSTRB;
    wire    [31:0]      m0_WDATA;
    
    wire                m0_BREADY, m0_BVALID;
    wire    [1:0]       m0_BRESP;
    
    wire                m0_ARVALID, m0_ARREADY;
    wire    [31:0]      m0_ARADDR;
    
    wire                m0_RREADY, m0_RVALID;
    wire    [1:0]       m0_RRESP;
    wire    [31:0]      m0_RDATA;
    
    
    /* slave 0 signals */
    wire                s0_AWVALID, s0_AWREADY;
    wire    [31:0]      s0_AWADDR;
    
    wire                s0_WVALID, s0_WREADY;
    wire    [3:0]       s0_WSTRB;
    wire    [31:0]      s0_WDATA;
    
    wire                s0_BREADY, s0_BVALID;
    wire    [1:0]       s0_BRESP;
    
    wire                s0_ARVALID, s0_ARREADY;
    wire    [31:0]      s0_ARADDR;
    
    wire                s0_RREADY, s0_RVALID;
    wire    [1:0]       s0_RRESP;
    wire    [31:0]      s0_RDATA;
    
    
    /* slave 1 signals */
    wire                s1_AWVALID, s1_AWREADY;
    wire    [31:0]      s1_AWADDR;
    
    wire                s1_WVALID, s1_WREADY;
    wire    [3:0]       s1_WSTRB;
    wire    [31:0]      s1_WDATA;
    
    wire                s1_BREADY, s1_BVALID;
    wire    [1:0]       s1_BRESP;
    
    wire                s1_ARVALID, s1_ARREADY;
    wire    [31:0]      s1_ARADDR;
    
    wire                s1_RREADY, s1_RVALID;
    wire    [1:0]       s1_RRESP;
    wire    [31:0]      s1_RDATA;
    
    
    /* slave 0 memory */
    wire    [1:0]       slave0_write_resp, slave0_read_resp;
    reg     [31:0]      write0_addr, read0_addr;
    reg     [31:0]      slave0_mem [0:255];
    wire                slave0_write_data_done;
    wire    [31:0]      slave0_read_data, slave0_write_addr, slave0_write_data, slave0_read_addr;
    wire                slave0_write_addr_done, slave0_read_addr_done;
    
    
    /* slave 1 memory */
    wire    [1:0]       slave1_write_resp, slave1_read_resp;
    reg     [31:0]      write1_addr, read1_addr;
    reg     [31:0]      slave1_mem [0:255];
    wire                slave1_write_data_done;
    wire    [31:0]      slave1_read_data, slave1_write_addr, slave1_write_data, slave1_read_addr;
    wire                slave1_write_addr_done, slave1_read_addr_done;
    
    
    integer         i;
    integer         idx, valid_idx, try_idx, found;
    integer         total_ops = 0;
    
    reg             has_written[0:24];
    reg     [31:0]  addr_list [0:24];
    reg     [31:0]  data_list [0:24];
    
    axi4_lite_master #(
        .ADDR_WIDTH(32), .DATA_WIDTH(32)
    ) u_master0 (
        .iCLK(iCLK), .iRST(iRST),
        
        /* write */
        .m_AWREADY(m0_AWREADY), .m_AWVALID(m0_AWVALID), .m_AWPROT(), .m_AWADDR(m0_AWADDR),
        .m_WREADY(m0_WREADY), .m_WVALID(m0_WVALID), .m_WDATA(m0_WDATA), .m_WSTRB(m0_WSTRB),
        .m_BVALID(m0_BVALID), .m_BRESP(m0_BRESP), .m_BREADY(m0_BREADY),
        
        /* read */
        .m_ARREADY(m0_ARREADY), .m_ARVALID(m0_ARVALID), .m_ARPROT(), .m_ARADDR(m0_ARADDR),
        .m_RVALID(m0_RVALID), .m_RRESP(m0_RRESP), .m_RDATA(m0_RDATA), .m_RREADY(m0_RREADY),
        
        /* interfaces */
        .write_req(m0_write_req), .write_addr(m0_write_addr), .write_data(m0_write_data), .write_strb(m0_write_strb), .write_resp(m0_write_resp),
        .read_req(m0_read_req), .read_addr(m0_read_addr), .read_data(m0_read_data), .read_resp(m0_read_resp)
    );
    
    axi4_lite_slave #(
        .ADDR_WIDTH(32), .DATA_WIDTH(32)
    ) u_slave0 (
        .iCLK(iCLK), .iRST(iRST),
        
        /* write */
        .s_AWVALID(s0_AWVALID), .s_AWPROT(3'b0), .s_AWADDR(s0_AWADDR), .s_AWREADY(s0_AWREADY),
        .s_WVALID(s0_WVALID), .s_WDATA(s0_WDATA), .s_WSTRB(s0_WSTRB), .s_WREADY(s0_WREADY),
        .s_BREADY(s0_BREADY), .s_BVALID(s0_BVALID), .s_BRESP(s0_BRESP),
        
        /* read */
        .s_ARVALID(s0_ARVALID), .s_ARPROT(3'b0), .s_ARADDR(s0_ARADDR), .s_ARREADY(s0_ARREADY),
        .s_RREADY(s0_RREADY), .s_RVALID(s0_RVALID), .s_RRESP(s0_RRESP), .s_RDATA(s0_RDATA),
        
        /* interfaces */
        .write_addr(slave0_write_addr), .write_data(slave0_write_data),.write_strb(slave0_write_strb), .write_resp(slave0_write_resp),
        .read_data(slave0_read_data), .read_addr(slave0_read_addr), .read_resp(slave0_read_resp)
    );
    
    axi4_lite_slave #(
        .ADDR_WIDTH(32), .DATA_WIDTH(32)
    ) u_slave1 (
        .iCLK(iCLK), .iRST(iRST),
        
        /* write */
        .s_AWVALID(s1_AWVALID), .s_AWPROT(3'b0), .s_AWADDR(s1_AWADDR), .s_AWREADY(s1_AWREADY),
        .s_WVALID(s1_WVALID), .s_WDATA(s1_WDATA), .s_WSTRB(s1_WSTRB), .s_WREADY(s1_WREADY),
        .s_BREADY(s1_BREADY), .s_BVALID(s1_BVALID), .s_BRESP(s1_BRESP),
        
        /* read */
        .s_ARVALID(s1_ARVALID), .s_ARPROT(3'b0), .s_ARADDR(s1_ARADDR), .s_ARREADY(s1_ARREADY),
        .s_RREADY(s1_RREADY), .s_RVALID(s1_RVALID), .s_RRESP(s1_RRESP), .s_RDATA(s1_RDATA),
        
        /* interfaces */
        .write_addr(slave1_write_addr), .write_data(slave1_write_data),.write_strb(slave1_write_strb), .write_resp(slave1_write_resp),
        .read_data(slave1_read_data), .read_addr(slave1_read_addr), .read_resp(slave1_read_resp)
    );
    
    axi4_lite_interconnect_m1s2 #(
        .LOW_ADDR0(LOW_ADDR0), .HIGH_ADDR0(HIGH_ADDR0),
        .LOW_ADDR1(LOW_ADDR1), .HIGH_ADDR1(HIGH_ADDR1)
    ) u_interconnect (
        .iCLK(iCLK), .iRST(iRST),
        
        /* master 0 signals */
        .m0_AWVALID(m0_AWVALID), .m0_AWADDR(m0_AWADDR), .m0_AWREADY(m0_AWREADY),
        .m0_WVALID(m0_WVALID), .m0_WSTRB(m0_WSTRB), .m0_WDATA(m0_WDATA), .m0_WREADY(m0_WREADY),
        .m0_BREADY(m0_BREADY), .m0_BVALID(m0_BVALID), .m0_BRESP(m0_BRESP),
        .m0_ARVALID(m0_ARVALID), .m0_ARADDR(m0_ARADDR), .m0_ARREADY(m0_ARREADY),
        .m0_RREADY(m0_RREADY), .m0_RVALID(m0_RVALID), .m0_RRESP(m0_RRESP), .m0_RDATA(m0_RDATA),
        
        /* slave 0 signals */
        .s0_AWREADY(s0_AWREADY), .s0_AWVALID(s0_AWVALID), .s0_AWADDR(s0_AWADDR),
        .s0_WREADY(s0_WREADY), .s0_WVALID(s0_WVALID), .s0_WSTRB(s0_WSTRB), .s0_WDATA(s0_WDATA),
        .s0_BVALID(s0_BVALID), .s0_BRESP(s0_BRESP), .s0_BREADY(s0_BREADY),
        .s0_ARREADY(s0_ARREADY), .s0_ARVALID(s0_ARVALID), .s0_ARADDR(s0_ARADDR), 
        .s0_RVALID(s0_RVALID), .s0_RRESP(s0_RRESP), .s0_RDATA(s0_RDATA), .s0_RREADY(s0_RREADY),

        /* slave 1 signals */
        .s1_AWREADY(s1_AWREADY), .s1_AWVALID(s1_AWVALID), .s1_AWADDR(s1_AWADDR),
        .s1_WREADY(s1_WREADY), .s1_WVALID(s1_WVALID), .s1_WSTRB(s1_WSTRB), .s1_WDATA(s1_WDATA),
        .s1_BVALID(s1_BVALID), .s1_BRESP(s1_BRESP), .s1_BREADY(s1_BREADY),
        .s1_ARREADY(s1_ARREADY), .s1_ARVALID(s1_ARVALID), .s1_ARADDR(s1_ARADDR), 
        .s1_RVALID(s1_RVALID), .s1_RRESP(s1_RRESP), .s1_RDATA(s1_RDATA), .s1_RREADY(s1_RREADY)
    );
    
    /* slave 0 memory model */
    always @(posedge iCLK) begin
        if (slave0_write_addr_done) write0_addr <= slave0_write_addr;
        if (slave0_write_data_done) slave0_mem[write0_addr] <= slave0_write_data;
        if (slave0_read_addr_done) read0_addr <= slave0_read_addr;
    end
    
    assign slave0_read_data         = slave0_mem[read0_addr];
    assign slave0_write_addr_done   = s0_AWVALID && s0_AWREADY;
    assign slave0_write_data_done   = s0_WVALID  && s0_WREADY;
    assign slave0_read_addr_done    = s0_ARVALID && s0_ARREADY;
    assign slave0_write_resp        = 2'b00;
    assign slave0_read_resp         = 2'b00;
    
    /* slave 1 memory model */
    always @(posedge iCLK) begin
        if (slave1_write_addr_done) write1_addr <= slave1_write_addr;
        if (slave1_write_data_done) slave1_mem[write1_addr] <= slave1_write_data;
        if (slave1_read_addr_done) read1_addr <= slave1_read_addr;
    end
    
    assign slave1_read_data         = slave1_mem[read1_addr];
    assign slave1_write_addr_done   = s1_AWVALID && s1_AWREADY;
    assign slave1_write_data_done   = s1_WVALID  && s1_WREADY;
    assign slave1_read_addr_done    = s1_ARVALID && s1_ARREADY;
    assign slave1_write_resp        = 2'b00;
    assign slave1_read_resp         = 2'b00;
    
    initial begin
        iCLK = 1'b1;
        forever #(CLK_PERIOD/2) iCLK = ~iCLK;
    end
    
    initial begin
        iRST             = 1'b0;
        m0_write_req     = 1'b0;
        m0_write_strb    = 4'b0;
        m0_write_addr    = 32'h0;
        m0_write_data    = 32'h0;
        m0_read_req      = 1'b0;
        m0_read_addr     = 32'h0;
    
        /* memory initialization */
        write0_addr      = 32'h0;
        read0_addr       = 32'h0;
        write1_addr      = 32'h0;
        read1_addr       = 32'h0;
    end
    
    /* generate address and data list */
    initial begin
        for (i = 0; i < 25; i = i + 1) begin
            if ($urandom % 2)
                addr_list[i] = 32'h00000100 + (($urandom % 64) * 4);
            else
                addr_list[i] = 32'h00000000 + (($urandom % 64) * 4);
            
            data_list[i] = $urandom;
        end
    end
    
    /* test case */
    initial begin
        $dumpfile("logical/sim/axi4_lite_interconnect/axi4_lite_interconnect_m1s2.vcd");
        $dumpvars(0, tb_axi4_lite_interconnect_m1s2);
    
        /* init memory */
        for (i = 0; i < 256; i = i + 1) begin
            slave0_mem[i] = 32'h0;
            slave1_mem[i] = 32'h0;
        end
    
        for (i = 0; i < 25; i = i + 1)
            has_written[i] = 1'b0;
    
        #10; iRST = 1'b1;
    
        $display("\n[INFO] Memulai simulasi AXI4-Lite Interconnect (random read/write)\n");
    
        while (total_ops < 50) begin
            if ($urandom_range(0, 1)) begin
                /* ================== WRITE ================== */
                
                idx = $urandom_range(0, 24);
    
                $display("[WRITE] Addr = 0x%08h, Data = 0x%08h", addr_list[idx], data_list[idx]);
    
                m0_write_addr       <= addr_list[idx];
                m0_write_data       <= data_list[idx];
                m0_write_strb       <= 4'b1111;
                m0_write_req        <= 1'b1;
    
                @(posedge m0_BREADY);
                    m0_write_req    <= 1'b0;
    
                has_written[idx]    = 1'b1;
    
            end else begin
                /* ================== READ ================== */
                found = 0;
    
                repeat (5) begin
                    try_idx = $urandom_range(0, 24);
    
                    if (has_written[try_idx]) begin
                        valid_idx   = try_idx;
                        found       = 1;
                    end
                end
    
                if (found) begin
                    $display("[READ ] Addr = 0x%08h", addr_list[valid_idx]);
    
                    m0_read_addr    <= addr_list[valid_idx];
                    m0_read_req     <= 1'b1;
    
                    @(posedge m0_RREADY);
                        m0_read_req <= 1'b0;
                end else begin
                    $display("[SKIP ] Tidak ada alamat yang valid untuk read");
                end
            end
    
            total_ops += 1;
        end
    
        $display("\n[INFO] Selesai semua test random read-write\n");
        $finish;
    end
    
endmodule