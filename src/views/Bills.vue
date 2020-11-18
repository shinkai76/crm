<template>
    <div id="bill">
        <div class="mainForm" ref="mainForm">
            <div class="item">
                <label>合同标题&nbsp;</label>
                <el-input v-model.trim="mainForm.title" placeholder="合同标题" clearable size="mini"></el-input>
            </div>
            <div class="item">
                <label>开始时间&nbsp;</label>
                <el-date-picker
                        size="mini"
                        value-format="yyyy-MM-dd HH:mm:ss"
                        v-model="mainForm.start_date"
                        type="date">
                </el-date-picker>
            </div>
            <div class="item">
                <label>截止时间&nbsp;</label>
                <el-date-picker
                        size="mini"
                        value-format="yyyy-MM-dd HH:mm:ss"
                        v-model="search_end_date"
                        type="date">
                </el-date-picker>
            </div>
            <div class="item">
                <label>合同类型&nbsp;</label>
                <el-select v-model="mainForm.category" clearable size="mini">
                    <el-option
                            v-for="item in categoryList"
                            :label="item.label"
                            :value="item.value">
                    </el-option>
                </el-select>
            </div>
            <div class="item">
                <label>合同状态&nbsp;</label>
                <el-select v-model="mainForm.status" clearable size="mini">
                    <el-option
                            v-for="item in statusList"
                            :label="item.label"
                            :value="item.value">
                    </el-option>
                </el-select>
            </div>
            <div class="item">
                <label>审批状态&nbsp;</label>
                <el-select v-model="mainForm.approve_status" clearable size="mini">
                    <el-option
                            v-for="item in approveStatusList"
                            :label="item.label"
                            :value="item.value">
                    </el-option>
                </el-select>
            </div>
            <div class="item">
                <label>导入状态&nbsp;</label>
                <el-select v-model="mainForm.is_imported" clearable size="mini">
                    <el-option label="已导入" value="1"></el-option>
                    <el-option label="未导入" value="0"></el-option>
                </el-select>
            </div>
            <div class="item">
                <label>下载状态&nbsp;</label>
                <el-select v-model="mainForm.is_completed" clearable placeholder="请选择" size="mini">
                    <el-option label="已下载" value="1"></el-option>
                    <el-option label="未下载" value="0"></el-option>
                </el-select>
            </div>
            <div class="item">
                <label>时间类型&nbsp;</label>
                <el-select v-model="mainForm.time_type" clearable size="mini">
                    <el-option label="审批时间" value="sign_date"></el-option>
                    <el-option label="创建时间" value="created_at"></el-option>
                    <el-option label="结束时间" value="end_at"></el-option>
                </el-select>
            </div>

        </div>
        <div class="btns" ref="btns">
            <el-button type="primary" size="mini" @click="searchOrder()" plain>查询</el-button>
            <el-button type="primary" size="mini" @click="showDownload = true" plain>下载合同列表</el-button>
            <el-button type="primary" size="mini" @click="downloadManually()" plain>手动下载合同</el-button>
            <el-button type="primary" size="mini" @click="resetStatus()" plain>状态重置</el-button>
            <el-button type="warning" size="mini" @click="importC8()" plain>导入C8</el-button>
            <el-button type="danger" size="mini" @click="deleteOrder()" plain>删除合同</el-button>
        </div>

        <div class="subTable">
            <el-table
                    @selection-change="handleSelectionChange"
                    ref="subTable"
                    size="mini"
                    border
                    stripe
                    :height="table_height"
                    :data="subTable"
                    empty-text="-"
                    tooltip-effect="dark"
                    style="width: 100%">
                <el-table-column
                        fixed
                        type="selection"
                        width="55">
                </el-table-column>
                <el-table-column type="expand" fixed>
                    <template slot-scope="{row}">
                        <span class="err" v-if="!row.product_assets_for_new_record.items.length">无商品明细</span>
                        <table class="table-inline" v-else>
                            <thead>
                            <tr>
                                <th>商品名称</th>
                                <th>产品码</th>
                                <th>商品数量</th>
                                <th>商品总价</th>
                            </tr>
                            </thead>
                            <tbody>
                            <tr v-for="pro in row.product_assets_for_new_record.items">
                                <td>{{pro.name}}</td>
                                <td class="t-center">{{pro.product_no}}</td>
                                <td class="t-right">{{pro.quantity}} {{ pro.sale_unit }}</td>
                                <td class="t-right">{{pro.total_price}}</td>
                            </tr>
                            </tbody>
                        </table>
                    </template>
                </el-table-column>
                <el-table-column
                        show-overflow-tooltip
                        header-align="center"
                        prop="sn"
                        label="合同编号"
                        width="160">
                </el-table-column>
                <el-table-column
                        show-overflow-tooltip
                        header-align="center"
                        prop="title"
                        label="合同标题"
                        width="200">
                </el-table-column>
                <el-table-column
                        align="center"
                        prop="category_mapped"
                        label="合同类型"
                        width="120">
                </el-table-column>
                <el-table-column
                        align="center"
                        prop="status_mapped"
                        label="状态"
                        width="120">
                </el-table-column>
                <el-table-column
                        header-align="center"
                        align="right"
                        prop="total_amount"
                        label="合同总金额"
                        width="120">
                </el-table-column>
                <el-table-column
                        align="center"
                        prop="approve_status_i18n"
                        label="审核状态"
                        width="120">
                </el-table-column>
                <el-table-column
                        header-align="center"
                        prop="sign_date"
                        label="签约日期"
                        width="160">
                </el-table-column>
                <el-table-column
                        align="center"
                        prop="creator.name"
                        label="创建者"
                        width="120">
                </el-table-column>
                <el-table-column
                        show-overflow-tooltip
                        header-align="center"
                        prop="customer.name"
                        label="客户信息"
                        width="160">
                </el-table-column>
                <el-table-column
                        header-align="center"
                        prop="sale_document_code"
                        label="销售订单单号"
                        width="180">
                </el-table-column>
                <el-table-column
                        align="center"
                        prop="is_imported"
                        label="是否已导入"
                        width="120">
                </el-table-column>
                <el-table-column
                        align="center"
                        prop="is_completed"
                        label="是否下载完成"
                        width="120">
                </el-table-column>
                <el-table-column
                        header-align="center"
                        prop="created_at"
                        label="合同创建时间"
                        width="160">
                </el-table-column>
                <el-table-column
                        header-align="center"
                        prop="updated_at"
                        label="合同更新时间"
                        width="160">
                </el-table-column>
                <el-table-column
                        header-align="center"
                        prop="imported_at"
                        label="导入时间"
                        width="160">
                </el-table-column>
                <el-table-column
                        header-align="center"
                        prop="download_at"
                        label="下载时间"
                        width="160">
                </el-table-column>
            </el-table>
        </div>
        <div class="pagination" ref="pagination">
            <el-pagination
                    @size-change="handleSizeChange"
                    @current-change="handleCurrentChange"
                    :current-page="currentPage"
                    :page-sizes="[30, 50, 100]"
                    :page-size="defalut_limit"
                    layout="total, sizes,prev, pager, next, jumper"
                    :total="totalSubTable">
            </el-pagination>
        </div>

        <!--下载弹窗-->
        <el-dialog title="下载合同" :visible.sync="showDownload" width="70%" class="downLoadDialog">
            <el-form :model="downloadForm" label-width="100px">
                <el-row :gutter="20">
                    <el-col :span="12">
                        <el-form-item label="合同标题">
                            <el-input v-model.trim="downloadForm.title" placeholder="合同标题" clearable size="mini"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="合同类型">
                            <el-select v-model="downloadForm.category" clearable size="mini" disabled>
                                <el-option
                                        v-for="item in categoryList"
                                        :label="item.label"
                                        :value="item.value">
                                </el-option>
                            </el-select>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row :gutter="20">
                    <el-col :span="12">
                        <el-form-item label="合同状态">
                            <el-select v-model="downloadForm.status" clearable size="mini">
                                <el-option
                                        v-for="item in statusList"
                                        :label="item.label"
                                        :value="item.value">
                                </el-option>
                            </el-select>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="审批状态">
                            <el-select v-model="downloadForm.approve_status" clearable size="mini">
                                <el-option
                                        v-for="item in approveStatusList"
                                        :label="item.label"
                                        :value="item.value">
                                </el-option>
                            </el-select>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row :gutter="20">
                    <el-col :span="12">
                        <el-form-item label="开始时间">
                            <el-date-picker
                                    style="width: 100%;"
                                    size="mini"
                                    value-format="yyyy-MM-dd HH:mm:ss"
                                    v-model="downloadForm.start_date"
                                    type="date">
                            </el-date-picker>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="截止时间">
                            <el-date-picker
                                    style="width: 100%;"
                                    size="mini"
                                    value-format="yyyy-MM-dd HH:mm:ss"
                                    v-model="down_end_date"
                                    type="date">
                            </el-date-picker>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row :gutter="20">
                    <el-col :span="12">
                        <el-form-item label="时间类型">
                            <el-select v-model="downloadForm.time_type" clearable size="mini">
                                <el-option label="审批时间" value="sign_date"></el-option>
                                <el-option label="创建时间" value="created_at"></el-option>
                                <el-option label="结束时间" value="end_at"></el-option>
                            </el-select>
                        </el-form-item>
                    </el-col>
                </el-row>
            </el-form>
            <div slot="footer" class="dialog-footer">
                <el-button @click="showDownload = false">取 消</el-button>
                <el-button type="primary" @click="startDownload()">确 定</el-button>
            </div>
        </el-dialog>
    </div>
</template>

<script>
  export default {
    name: "bills",
    data() {
      return {
        table_height: 500,
        totalSubTable: 0,
        defalut_limit: 50,
        new_start: 0,
        mainForm: {
          category: "",
          status: "",
          approve_status: "",
          start_date: "",
          end_date: "",
          title: "",
          is_imported: "",
          is_completed: "",
          start: "",
          limit: "",
          time_type: ""
        },
        categoryList: [
          {
            label: "不限",
            value: ""
          }, {
            label: "销售合同",
            value: "10730677"
          }, {
            label: "项目合同",
            value: "10730678"
          }, {
            label: "采购合同",
            value: "10730679"
          }, {
            label: "服务合同",
            value: "10730680"
          }, {
            label: "其他",
            value: "10730681"
          }
        ],
        statusList: [
          {
            label: "不限",
            value: ""
          }, {
            label: "未开始",
            value: "10730686"
          }, {
            label: "执行中",
            value: "10730687"
          }, {
            label: "成功结束",
            value: "10730688"
          }, {
            label: "意外终止",
            value: "10730689"
          }, {
            label: "货先交，补合同",
            value: "10849211"
          }, {
            label: "其他",
            value: "10849212"
          }
        ],
        approveStatusList: [
          {
            label: "不限",
            value: ""
          }, {
            label: "已撤销",
            value: "reverted"
          }, {
            label: "已否决",
            value: "rejected"
          }, {
            label: "待1级审批",
            value: 1
          }, {
            label: "待2级审批",
            value: 2
          }, {
            label: "已通过",
            value: "approved"
          }
        ],
        timeTypeList: [
          {
            label: "审批时间",
            value: "sign_date"
          }, {
            label: "创建时间",
            value: "created_at"
          }, {
            label: "结束时间",
            value: "end_at"
          }
        ],
        subTable: [],
        multipleSelection: [], // 多选 选中的行
        currentPage: 1,
        id_arr: [],
        showDownload: false,
        down_end_date: "",
        search_end_date: "",
        downloadForm: {
          category: "10730677",
          status: "",
          approve_status: "approved",
          end_date: "",
          start_date: "",
          title: "",
          time_type: "created_at"
        }
      }
    },
    mounted() {
      this.setDefaultDate()
      this.searchOrder()
      this.$nextTick(() => {
        let autoHeight = document.documentElement.clientHeight
                        - this.$refs.btns.offsetHeight
                        - this.$refs.mainForm.offsetHeight
                        - this.$refs.pagination.offsetHeight
                        - 64
        this.table_height = autoHeight
      });
    },
    methods: {
      setDefaultDate() { // 本月1号至今
        var myDate = new Date()
        let year = myDate.getFullYear()
        let month = myDate.getMonth() + 1
        let date = myDate.getDate() + 1
        let sTime = new Date(`${year}-${month}-01`)
        this.mainForm.start_date = sTime
        this.downloadForm.start_date = sTime
        // 展示在界面上的截止日期
        this.down_end_date = new Date(`${year}-${month}-${date - 1}`)
        this.search_end_date = new Date(`${year}-${month}-${date - 1}`)
      },
      startDownload() {
        this.showDownload = false
        this.downloadOrder()
      },
      handleSizeChange(val) {
        this.defalut_limit = val
      },
      handleCurrentChange(val) {
        this.currentPage = val || this.currentPage
        this.new_start = ( this.currentPage - 1 ) * this.defalut_limit
        this.searchOrder()
      },
      handleSelectionChange(val) { // 多选
        this.multipleSelection = val;
      },
      getSelectedID() {
        if ( !this.multipleSelection.length ) {
          alert("请至少选中一行")
          return false
        }
        this.id_arr = []
        this.multipleSelection.forEach((val) => {
          this.id_arr.push(val.id)
        })
        return true
      },
      downloadOrder(page = 1) { // 下载crm合同列表
        let params = JSON.parse(JSON.stringify(this.downloadForm))
        params.page = page
        params.per_page = 50
        params.end_date = this.addDate(this.down_end_date)
        this.$axios({
          url: `/api/orders?action=get_orders`,
          params: params,
        }).then(res => {
          if (res.state ===1) {
            if (res.page) {
              this.downloadOrder(page ++)
            }
            if (res.page == null){
              this.$notify({
                title: "下载列表完成",
                type: "success"
              });
            }
            return
          }
          alert(res.errmsg)
        })
      },
      downloadManually() { // 手动下载合同
        this.ajaxFunction("complete_download", "GET", "手动下载合同")
      },
      deleteOrder() { // 删除合同
        this.ajaxFunction(null, "DELETE", "删除合同", "/api/orders/")
      },
      resetStatus() { // 状态重置
        this.ajaxFunction("init_order", "GET", "重置状态")
      },
      importC8() { // 导入c8生成销售订单
        this.ajaxFunction("import", "GET", "导入C8")
      },
      async ajaxFunction(action, method, text, url = "") {
        if ( !this.getSelectedID() ) return
        let count_failed = 0
        let count_succeed = 0
        let _total = 0
        for await ( let id of this.id_arr ) {
          this.$axios({
            method: method,
            url: url? url + id : `/api/orders/${id}?action=${action}`
          }).then(res => {
            if ( res.state === 1 ) {
              count_succeed++
              return
            }
            count_failed++
            alert(res.errmsg)
          }).finally(() => {
            _total++
            if ( _total == this.id_arr.length ) {
              alert(`共${this.id_arr.length}条，成功${text}${count_succeed}条，失败${count_failed}条`)
            }
          })
        }
        this.handleCurrentChange(1)
        this.multipleSelection = []
      },
      addDate(end_date) {
        var _end_date = new Date(end_date)
        var millSeconds = Math.abs(_end_date) + (24 * 60 * 60 * 1000)
        var added = new Date(millSeconds)
        let year = added.getFullYear()
        let month = added.getMonth() + 1
        let date = added.getDate()
        let eTime = new Date(`${year}-${month}-${date}`)
        return eTime
      },
      searchOrder() { // 查询crm合同
        this.mainForm.limit = this.defalut_limit
        this.mainForm.start = this.new_start
        let params = JSON.parse(JSON.stringify(this.mainForm))
        params.end_date = this.addDate(this.search_end_date)
        this.$axios({
          url: "/api/orders?action=trade_view",
          params: params
        }).then(res => {
          if ( res.state === 1 ) {
            this.totalSubTable = Number(res.total)
            res.root.forEach((val) => {
              for ( let keyName in val ) {
                val[keyName] = val[keyName] == null ? "" : val[keyName]
                if ( typeof val[keyName] === "boolean" ) {
                  val[keyName] = val[keyName] == true ? "是" : "否"
                }
              }
            })
            this.subTable = res.root
            return
          }
          alert(res.errmsg)
        })
      }
    }
  }
</script>

<style scoped lang="less">
#bill, .mainForm {
    overflow: hidden;
}
.mainForm {
    .item {
        float: left;
        overflow: hidden;
        width: 300px;
        margin: 2px 0;
        label {
            width: 100px;
            text-align: right;
            display: inline-block;
        }
        .el-input, .el-select {
            width: 200px;
        }
    }
}
.btns {
    width: 100%;
    margin: 4px 0;
    padding: 0 10px;
}
.subTable {
    .table-inline {
        width: 50%;
        margin-left: 43px;
        padding-left: 8px;
        background-color: #409EFF;
        text-align: center;
        th {
            text-align: center;
        }
        th:first-child {
            width: 40%;
        }
        .t-right {
            text-align: right;
        }
        .t-center {
            text-align: center;
        }
    }
    .err {
        color: red;
    }
    .el-table--mini td, .el-table--mini th {
        padding: 4px 0;
    }
}
.downLoadDialog {
    .el-form-item {
        margin-bottom: 0;
    }
}
</style>