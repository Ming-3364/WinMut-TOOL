<template>
<el-container style="height: 100%;">
  <!-- side bar -->
  <el-aside width="200px">
    <!-- subject selector -->
    <el-dropdown @command="selectSubject" style="margin-bottom: 40px;">
      <el-button type="primary">
        Subject<i class="el-icon-arrow-down el-icon--right"></i>
        {{ curSubject }}
      </el-button>
      <el-dropdown-menu slot="dropdown">
        <el-dropdown-item command="demo">Demo</el-dropdown-item>
        <el-dropdown-item>Pcre2</el-dropdown-item>
        <el-dropdown-item>Grep</el-dropdown-item>
        <el-dropdown-item disabled>Coreutils</el-dropdown-item>
        <el-dropdown-item divided>xxx</el-dropdown-item>
      </el-dropdown-menu>
    </el-dropdown>

    <!-- subject foleders -->
    <el-tree style="border: 1px solid #ccc; border-radius: 4px;  box-shadow: 0 2px 4px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .04)"
        :data="foldersData"
        @node-click="handleFileClick"
      >
    </el-tree>
    <!-- <el-menu
      style="height: 100%;"
      @select="handleMutOutputFileSelect"
      :default-active="activeFileGroupIndex"
    >
    <el-menu-item 
      v-for="file in files" 
      :key="file.name" 
      :index="file.name"
      @click="handleSelectMutOutputFile(file)"
    >
      {{ file.name }}
    </el-menu-item>
    </el-menu> -->
  </el-aside>

  <!-- run, code, and result -->
  <el-container>

    <!-- run -->
    <el-header>
      <el-row type="flex" justify="space-between">
        <!-- 左对齐的按钮组 -->
        <el-col>
          <el-button type="primary" @click="runCaseConfigDrawer = true">Run Case Config</el-button>
          <el-drawer
            title="Run Case Config"
            :visible.sync="runCaseConfigDrawer"
            :direction="runCaseConfigDrawerDirection"
            size='55%'
            :before-close="handleClose">
            <el-form :model="runCaseConfigForm" ref="runCaseConfigForm" label-width="100px" class="demo-dynamic">
              <el-form-item
                v-for="(runCase, index) in runCaseConfigForm"
                :label="'Case' + (index+1)"
                :key="runCase.key"
                :rules="{
                }"
              >
                <el-form :inline="true" :model="runCaseConfigForm[index]" class="demo-form-inline">
                  <el-form-item label="file">
                    <!-- TODO: rule for check input run case config -->
                    <el-select v-model="runCase.file" placeholder="file">
                      <el-option 
                        v-for="file in foldersData"
                        :label=file.label
                        :key=file.label
                        :value="file.label | reversedMessage"
                      >
                      </el-option>
                    </el-select>
                  </el-form-item>
                  <el-form-item label="argvs">
                    <el-input v-model="runCase.argv" placeholder="argvs"></el-input>
                  </el-form-item>
                  
                  <el-form-item>
                    <el-button type="primary" @click="delRunCase(index)">删除</el-button>
                  </el-form-item>
                </el-form>
              </el-form-item>
              <el-form-item>
                <el-button  type="primary" @click="addRunCase">新增</el-button>
                <el-button  type="primary" @click="resetRunCase()">重置</el-button>
              </el-form-item>
            </el-form>
            <!-- {{ runCaseConfigForm }}
            {{ defaultRunCaseConfigForm }} -->

          </el-drawer>
        </el-col>

        <!-- 右对齐的按钮组 -->
        <el-col style="text-align: right;">
          <el-button type="primary" @click="submitRunCaseConfigForm">Run</el-button>
        </el-col>
      </el-row>
    </el-header>

    <!-- code and result -->
    <el-container>

      <!-- code -->
      <el-main style="width: 50%;">
        <el-input v-if="!sourceFileLoading"
          type="textarea" 
          :rows="32"
          placeholder="Please select a source file."
          v-model="cur_file_content"
          show-password
        ></el-input>
        <el-skeleton v-else :rows="20" animated />
      <!-- <el-empty v-else
        description="Please select a source file."
      ></el-empty> -->
      </el-main>

      <!-- result -->
      <el-main style="width: 50%; " >
        <el-tabs type="border-card" stretch="true" style="height: 90%;" >

          <!-- OUTPUT -->
          <el-tab-pane label="OUTPUT" v-loading="running">
            <el-tabs v-model="activeOutputTab" style="height: 90%;" v-if="Object.keys(mutOutputFilesForRun).length !== 0">
              <el-tab-pane
                v-for="(mutOutputFilesForCase, caseName, index) in mutOutputFilesForRun"
                :label="caseName"
                :name="caseName"
                :key="index"
                style="height: 100%;"
              >
                <!-- tab content -->
                <el-container style="height: 100%;">
                  <!-- 左侧文件选择栏 -->
                  <el-aside width="200px"  style="height: 100%;">
                  <el-scrollbar  style="height: 500px;">
                    <el-menu
                      style="height: 100%;"
                      @select="handleMutOutputFileSelect"
                      :default-active="activeFileGroupIndex"
                    >
                      <el-submenu
                        v-for="(files, fileGroup, index) in mutOutputFilesForCase.mutOutputFiles"
                        :title="fileGroup"
                        :key="index"
                        :index="index"
                      >
                        <!-- <template slot="title"> -->
                          <!-- <i class="el-icon-location"></i> -->
                          <span slot="title">{{fileGroup}}</span>
                        <!-- </template> -->
                        <el-menu-item 
                          v-for="file in files" 
                          :key="file.name" 
                          :index="file.name"
                          @click="handleSelectMutOutputFile(file)"
                        >
                          {{ file.name }}
                        </el-menu-item>
                      </el-submenu>
                    </el-menu>
                  </el-scrollbar>
                  </el-aside>

                  <!-- 右侧文件内容显示区域 -->
                  <el-main>
                    <!-- <codemirror v-model="selectedMutOutputContent" :options="editorOptions">{{selectedMutOutputContent}}</codemirror> -->
                    <el-input v-if="!mutOutputLoading"
                      type="textarea"
                      :rows="22"
                      placeholder="Please select a mut output file."
                      v-model="selectedMutOutputContent"

                      :disabled="false"
                    >
                    </el-input>
                    <el-skeleton v-else :rows="10" animated />
                    <!-- <el-empty v-else
                      description="Please select a mut output file."
                    > -->
                    <!-- </el-empty> -->
                  </el-main>
                </el-container>
              </el-tab-pane>
            </el-tabs>
            <el-empty v-else style="margin-top: 80px;"
              description="No output, please run first"
            ></el-empty>
          </el-tab-pane>
          
          <!-- STATS -->
          <el-tab-pane label="STATS" v-loading="running">
            <el-tabs v-model="activeStatTab" style="height: 90%;">
              <el-tab-pane
                label="Summary"
                name="Summary"
                key="Summary"
                style="height: 90%;"
              >
              <!-- {{ runStat.Summary }} -->
              <!-- <div> -->
                <el-table :data="runStat.Summary">
                  <el-table-column
                    prop="label"
                    label=""
                    width="180">
                  </el-table-column>
                  <el-table-column
                    prop="ms_k2g"
                    label="ms_k2g"
                    width="180">
                  </el-table-column>
                  <el-table-column
                    prop="ms_k2c"
                    label="ms_k2c"
                    width="180">
                  </el-table-column>
                </el-table>
              <!-- </div> -->
              </el-tab-pane>

              <el-tab-pane
                
                v-for="(caseInfo, caseName) in runStat.MACases"
                :label="caseName"
                :name="caseName"
                :key="caseName"
                style="height: 90%;"
              >
              <!-- {{ caseInfo }} -->
                <el-table :data="caseInfo" 
                  height="500"
                  border
                  show-header="false"
                >
                  <el-table-column
                    prop="label"
                    label="Label"
                    width="270">
                  </el-table-column>
                  <el-table-column
                    prop="value"
                    label="Value"
                    width="270">
                  </el-table-column>
                </el-table>
              </el-tab-pane>
            </el-tabs>
          </el-tab-pane>

        </el-tabs>
      </el-main>

    </el-container>
    
  </el-container>
</el-container>
</template>

<!-- <template>
<div id="app" style="height: 100vh;">
<el-row style="height: 100vh;">
  <el-col :span="12"><div class="grid-content bg-purple">main1</div></el-col>
  <el-col :span="12"><div class="grid-content bg-purple-light">main2</div></el-col>
</el-row>
<el-row style="height: 100vh;">
  <el-col :span="8"><div class="grid-content bg-purple">main3</div></el-col>
  <el-col :span="8"><div class="grid-content bg-purple-light">main4</div></el-col>
  <el-col :span="8"><div class="grid-content bg-purple">main5</div></el-col>
</el-row>
</div>
</template> -->

<style scoped>
* {
  /* border: 1px solid #ddd; */
}




</style>

<script>
// import codemirror
// import { codemirror } from 'vue-codemirror';
import 'codemirror/lib/codemirror.css';

export default {
  data() {
    return {
      curSubject: "demo",
      // subject folders
      foldersData: [
        {
          id: 1,
          label: 'file1',
        },
        {
          id: 2,
          label: 'file2',
        },
        {
          id: 3,
          label: 'file5',
        }
      ],
      selectedNodeLabel: '',

      // code
      cur_file_content: '',
      sourceFileLoading: false,

      // run case config
      runCaseConfigDrawer: false,
      runCaseConfigDrawerDirection: 'ttb',
      runCaseConfigForm: [],
      // defaultRunCaseConfigForm: [
      //   {
      //     file: 'quick_sort',
      //     argv: '44 55 66 11 22 33'
      //   },
      //   {
      //     file: 'bubble_sort',
      //     argv: '44 55 66 11 22 33'
      //   },
      //   {
      //     file: 'reverse_string',
      //     argv: 'Hello World!'
      //   },
      //   {
      //     file: 'fibonacci',
      //     argv: '7'
      //   },
      //   {
      //     file: 'mut_output-carrymut',
      //     argv: ''
      //   },
      // ],
      defaultRunCaseConfigForm: [
        // quick_sort
        {
          file: 'quick_sort',
          argv: '42'
        },
        {
          file: 'quick_sort',
          argv: '44 55 66 11 22 33'
        },
        {
          file: 'quick_sort',
          argv: '1 2 3 4 5'
        },
        {
          file: 'quick_sort',
          argv: '9 8 7 6 5 4 3 2 1'
        },
        {
          file: 'quick_sort',
          argv: '3 3 1 4 2 2 5 1'
        },
        // bubble_sort
        {
          file: 'bubble_sort',
          argv: '42'
        },
        {
          file: 'bubble_sort',
          argv: '44 55 66 11 22 33'
        },
        {
          file: 'bubble_sort',
          argv: '1 2 3 4 5'
        },
        {
          file: 'bubble_sort',
          argv: '9 8 7 6 5 4 3 2 1'
        },
        {
          file: 'bubble_sort',
          argv: '3 3 1 4 2 2 5 1'
        },
        // reverse_string
        {
          file: 'reverse_string',
          argv: 'Hello World!'
        },
        {
          file: 'reverse_string',
          argv: '""'
        },
        {
          file: 'reverse_string',
          argv: '123!@#abc'
        },
        {
          file: 'reverse_string',
          argv: 'This is a long string with multiple words and spaces.'
        },
        {
          file: 'reverse_string',
          argv: 'aaaa'
        },
        {
          file: 'fibonacci',
          argv: '7'
        },
        {
          file: 'fibonacci',
          argv: '1'
        },
        {
          file: 'fibonacci',
          argv: '2'
        },
        {
          file: 'fibonacci',
          argv: '3'
        },
        {
          file: 'fibonacci',
          argv: '4'
        },
        {
          file: 'mut_output-carrymut',
          argv: ''
        },
      ],

      running: false,

      // OUTPUT
      activeOutputTab: 'case_1', // 设置默认激活的标签
      mutOutputFilesForRun: {},
      // mutOutputFilesForRun: {
      //   "case_1": {
      //         "case_dir": "/home/bjtucs/Desktop/Ming-18811237867/new/WinMutASE21Artifact-main/experiments/web-tool/web-run/2024-01-15-20-13-05/log/run/case_1",
      //         "mutOutputFiles": {
      //             "stdoutcopy": [
      //                 {
      //                     "name": "mut_output-0-stdoutcopy",
      //                     "path": "/home/bjtucs/Desktop/Ming-18811237867/new/WinMutASE21Artifact-main/experiments/web-tool/web-run/2024-01-15-20-13-05/log/run/case_1/mut_output-0-stdoutcopy"
      //                 },
      //                 {
      //                     "name": "mut_output-339-stdoutcopy",
      //                     "path": "/home/bjtucs/Desktop/Ming-18811237867/new/WinMutASE21Artifact-main/experiments/web-tool/web-run/2024-01-15-20-13-05/log/run/case_1/mut_output-339-stdoutcopy"
      //                 },
      //                 {
      //                     "name": "mut_output-339-stdoutcopy",
      //                     "path": "/home/bjtucs/Desktop/Ming-18811237867/new/WinMutASE21Artifact-main/experiments/web-tool/web-run/2024-01-15-20-13-05/log/run/case_1/mut_output-339-stdoutcopy"
      //                 },
      //                 {
      //                     "name": "mut_output-339-stdoutcopy",
      //                     "path": "/home/bjtucs/Desktop/Ming-18811237867/new/WinMutASE21Artifact-main/experiments/web-tool/web-run/2024-01-15-20-13-05/log/run/case_1/mut_output-339-stdoutcopy"
      //                 },
      //                 {
      //                     "name": "mut_output-339-stdoutcopy",
      //                     "path": "/home/bjtucs/Desktop/Ming-18811237867/new/WinMutASE21Artifact-main/experiments/web-tool/web-run/2024-01-15-20-13-05/log/run/case_1/mut_output-339-stdoutcopy"
      //                 },
      //                 {
      //                     "name": "mut_output-339-stdoutcopy",
      //                     "path": "/home/bjtucs/Desktop/Ming-18811237867/new/WinMutASE21Artifact-main/experiments/web-tool/web-run/2024-01-15-20-13-05/log/run/case_1/mut_output-339-stdoutcopy"
      //                 },
      //                 {
      //                     "name": "mut_output-339-stdoutcopy",
      //                     "path": "/home/bjtucs/Desktop/Ming-18811237867/new/WinMutASE21Artifact-main/experiments/web-tool/web-run/2024-01-15-20-13-05/log/run/case_1/mut_output-339-stdoutcopy"
      //                 },
      //                 {
      //                     "name": "mut_output-339-stdoutcopy",
      //                     "path": "/home/bjtucs/Desktop/Ming-18811237867/new/WinMutASE21Artifact-main/experiments/web-tool/web-run/2024-01-15-20-13-05/log/run/case_1/mut_output-339-stdoutcopy"
      //                 },
      //                 {
      //                     "name": "mut_output-339-stdoutcopy",
      //                     "path": "/home/bjtucs/Desktop/Ming-18811237867/new/WinMutASE21Artifact-main/experiments/web-tool/web-run/2024-01-15-20-13-05/log/run/case_1/mut_output-339-stdoutcopy"
      //                 },
      //                 {
      //                     "name": "mut_output-339-stdoutcopy",
      //                     "path": "/home/bjtucs/Desktop/Ming-18811237867/new/WinMutASE21Artifact-main/experiments/web-tool/web-run/2024-01-15-20-13-05/log/run/case_1/mut_output-339-stdoutcopy"
      //                 },
      //                 {
      //                     "name": "mut_output-339-stdoutcopy",
      //                     "path": "/home/bjtucs/Desktop/Ming-18811237867/new/WinMutASE21Artifact-main/experiments/web-tool/web-run/2024-01-15-20-13-05/log/run/case_1/mut_output-339-stdoutcopy"
      //                 },
      //                 {
      //                     "name": "mut_output-339-stdoutcopy",
      //                     "path": "/home/bjtucs/Desktop/Ming-18811237867/new/WinMutASE21Artifact-main/experiments/web-tool/web-run/2024-01-15-20-13-05/log/run/case_1/mut_output-339-stdoutcopy"
      //                 },
      //                 {
      //                     "name": "mut_output-339-stdoutcopy",
      //                     "path": "/home/bjtucs/Desktop/Ming-18811237867/new/WinMutASE21Artifact-main/experiments/web-tool/web-run/2024-01-15-20-13-05/log/run/case_1/mut_output-339-stdoutcopy"
      //                 },
      //                 {
      //                     "name": "mut_output-339-stdoutcopy",
      //                     "path": "/home/bjtucs/Desktop/Ming-18811237867/new/WinMutASE21Artifact-main/experiments/web-tool/web-run/2024-01-15-20-13-05/log/run/case_1/mut_output-339-stdoutcopy"
      //                 },
      //                 {
      //                     "name": "mut_output-339-stdoutcopy",
      //                     "path": "/home/bjtucs/Desktop/Ming-18811237867/new/WinMutASE21Artifact-main/experiments/web-tool/web-run/2024-01-15-20-13-05/log/run/case_1/mut_output-339-stdoutcopy"
      //                 },
      //                 {
      //                     "name": "mut_output-339-stdoutcopy",
      //                     "path": "/home/bjtucs/Desktop/Ming-18811237867/new/WinMutASE21Artifact-main/experiments/web-tool/web-run/2024-01-15-20-13-05/log/run/case_1/mut_output-339-stdoutcopy"
      //                 },
      //                 {
      //                     "name": "mut_output-339-stdoutcopy",
      //                     "path": "/home/bjtucs/Desktop/Ming-18811237867/new/WinMutASE21Artifact-main/experiments/web-tool/web-run/2024-01-15-20-13-05/log/run/case_1/mut_output-339-stdoutcopy"
      //                 },
      //                 {
      //                     "name": "mut_output-339-stdoutcopy",
      //                     "path": "/home/bjtucs/Desktop/Ming-18811237867/new/WinMutASE21Artifact-main/experiments/web-tool/web-run/2024-01-15-20-13-05/log/run/case_1/mut_output-339-stdoutcopy"
      //                 },
      //                 {
      //                     "name": "mut_output-339-stdoutcopy",
      //                     "path": "/home/bjtucs/Desktop/Ming-18811237867/new/WinMutASE21Artifact-main/experiments/web-tool/web-run/2024-01-15-20-13-05/log/run/case_1/mut_output-339-stdoutcopy"
      //                 },
      //                 {
      //                     "name": "mut_output-339-stdoutcopy",
      //                     "path": "/home/bjtucs/Desktop/Ming-18811237867/new/WinMutASE21Artifact-main/experiments/web-tool/web-run/2024-01-15-20-13-05/log/run/case_1/mut_output-339-stdoutcopy"
      //                 },
      //                 {
      //                     "name": "mut_output-339-stdoutcopy",
      //                     "path": "/home/bjtucs/Desktop/Ming-18811237867/new/WinMutASE21Artifact-main/experiments/web-tool/web-run/2024-01-15-20-13-05/log/run/case_1/mut_output-339-stdoutcopy"
      //                 },
      //             ]
      //     }
      //   },
      //   "case_2": {
      //         "case_dir": "/home/bjtucs/Desktop/Ming-18811237867/new/WinMutASE21Artifact-main/experiments/web-tool/web-run/2024-01-15-20-13-05/log/run/case_1",
      //         "mutOutputFiles": {
      //             "stdoutcopy": [
      //                 {
      //                     "name": "mut_output-0-stdoutcopy",
      //                     "path": "/home/bjtucs/Desktop/Ming-18811237867/new/WinMutASE21Artifact-main/experiments/web-tool/web-run/2024-01-15-20-13-05/log/run/case_1/mut_output-0-stdoutcopy"
      //                 },
      //                 {
      //                     "name": "mut_output-339-stdoutcopy",
      //                     "path": "/home/bjtucs/Desktop/Ming-18811237867/new/WinMutASE21Artifact-main/experiments/web-tool/web-run/2024-01-15-20-13-05/log/run/case_1/mut_output-339-stdoutcopy"
      //                 },
      //             ]
      //     }
      //   },
      // },
      activeFileGroupIndex: '0',
      selectedMutOutputContent: '',
      mutOutputLoading:false,

      // STATS
      runStat: {},
      // runStat: {
      //   "MACases": {
      //       "case_1": [
      //           {
      //               "label": "case_name",
      //               "value": "./bin/quick_sort 11 22 33 44 55 66"
      //           },
      //           {
      //               "label": "generated",
      //               "value": 20
      //           },
      //           {
      //               "label": "killed",
      //               "value": 3
      //           },
      //           {
      //               "label": "uncovered",
      //               "value": 10
      //           },
      //           {
      //               "label": "covered",
      //               "value": 10
      //           },
      //           {
      //               "label": "ms_k2g",
      //               "value": 0.15
      //           },
      //           {
      //               "label": "ms_k2c",
      //               "value": 0.3
      //           },
      //           {
      //               "label": "killed_by_proc_output",
      //               "value": 3
      //           },
      //           {
      //               "label": "killed_by_proc_end_status",
      //               "value": 0
      //           },
      //           {
      //               "label": "killed_by_both",
      //               "value": 0
      //           },
      //           {
      //               "label": "survived_not_affect_status",
      //               "value": 7
      //           },
      //           {
      //               "label": "survived_not_affect_output",
      //               "value": 5
      //           },
      //           {
      //               "label": "survived_by_both",
      //               "value": 5
      //           },
      //           {
      //               "label": "survived_not_covered",
      //               "value": 10
      //           }
      //       ],
      //       "case_2": [
      //           {
      //               "label": "case_name",
      //               "value": "./bin/quick_sort 11 22 33 44 55 66"
      //           },
      //           {
      //               "label": "generated",
      //               "value": 20
      //           },
      //           {
      //               "label": "killed",
      //               "value": 3
      //           },
      //           {
      //               "label": "uncovered",
      //               "value": 10
      //           },
      //           {
      //               "label": "covered",
      //               "value": 10
      //           },
      //           {
      //               "label": "ms_k2g",
      //               "value": 0.15
      //           },
      //           {
      //               "label": "ms_k2c",
      //               "value": 0.3
      //           },
      //           {
      //               "label": "killed_by_proc_output",
      //               "value": 3
      //           },
      //           {
      //               "label": "killed_by_proc_end_status",
      //               "value": 0
      //           },
      //           {
      //               "label": "killed_by_both",
      //               "value": 0
      //           },
      //           {
      //               "label": "survived_not_affect_status",
      //               "value": 7
      //           },
      //           {
      //               "label": "survived_not_affect_output",
      //               "value": 5
      //           },
      //           {
      //               "label": "survived_by_both",
      //               "value": 5
      //           },
      //           {
      //               "label": "survived_not_covered",
      //               "value": 10
      //           }
      //       ]
      //   },
      //   "Summary": [
      //       {
      //           "label": "ms_min",
      //           "ms_k2c": 0.3,
      //           "ms_k2g": 0.15
      //       },
      //       {
      //           "label": "ms_med",
      //           "ms_k2c": 0.3,
      //           "ms_k2g": 0.15
      //       },
      //       {
      //           "label": "ms_max",
      //           "ms_k2c": 0.3,
      //           "ms_k2g": 0.15
      //       },
      //       {
      //           "label": "ms_avg",
      //           "ms_k2c": 0.3,
      //           "ms_k2g": 0.15
      //       }
      //   ]
      // },

      activeStatTab: 'Summary',
      // runStat: {
      //   "MACases": {
      //       "case_2": {
      //           "case_name": "./bin/demo-fibonacci",
      //           "covered": 85,
      //           "generated": 85,
      //           "killed": 76,
      //           "killed_by_both": 20,
      //           "killed_by_proc_end_status": 20,
      //           "killed_by_proc_output": 76,
      //           "ms_k2c": 0.8941176470588236,
      //           "ms_k2g": 0.8941176470588236,
      //           "survived_by_both": 0,
      //           "survived_not_affect_output": 0,
      //           "survived_not_affect_status": 9,
      //           "survived_not_covered": 0,
      //           "uncovered": 0
      //       },
      //       "case_3": {
      //           "case_name": "./bin/demo-mut_output-carrymut",
      //           "covered": 39,
      //           "generated": 39,
      //           "killed": 31,
      //           "killed_by_both": 15,
      //           "killed_by_proc_end_status": 15,
      //           "killed_by_proc_output": 31,
      //           "ms_k2c": 0.7948717948717948,
      //           "ms_k2g": 0.7948717948717948,
      //           "survived_by_both": 0,
      //           "survived_not_affect_output": 0,
      //           "survived_not_affect_status": 8,
      //           "survived_not_covered": 0,
      //           "uncovered": 0
      //       },
      //       "case_4": {
      //           "case_name": "./bin/demo-quick_sort",
      //           "covered": 373,
      //           "generated": 794,
      //           "killed": 285,
      //           "killed_by_both": 175,
      //           "killed_by_proc_end_status": 175,
      //           "killed_by_proc_output": 285,
      //           "ms_k2c": 0.7640750670241286,
      //           "ms_k2g": 0.3589420654911839,
      //           "survived_by_both": 12,
      //           "survived_not_affect_output": 12,
      //           "survived_not_affect_status": 88,
      //           "survived_not_covered": 421,
      //           "uncovered": 421
      //       }
      //   },
      //   "Summary": {
      //       "ms_k2c_avg": 0.8176881696515824,
      //       "ms_k2c_max": 0.8941176470588236,
      //       "ms_k2c_med": 0.7948717948717948,
      //       "ms_k2c_min": 0.7640750670241286,
      //       "ms_k2g_avg": 0.6826438358072675,
      //       "ms_k2g_max": 0.8941176470588236,
      //       "ms_k2g_med": 0.7948717948717948,
      //       "ms_k2g_min": 0.3589420654911839
      //   }
      // }
    };
  },
  mounted() {
    // init run case config form
    this.runCaseConfigForm = [].concat(this.defaultRunCaseConfigForm);
    this.selectSubject("demo")
  },


  filters: {

    reversedMessage: function (str) {
      // 使用正则表达式匹配末尾的.c或.cpp，并替换为空字符串
      return str.replace(/\.c$|\.cpp$/, '');
    },

    capitalize: function (value) {
      if (!value) return ''
      value = value.toString()
      return value.charAt(0).toUpperCase() + value.slice(1)
    }
  },

  

  methods: {

    handleMutOutputFileSelect(){

    },

    handleSelectMutOutputFile(file){
      this.mutOutputLoading = true
      this.$axios.post('/api/get_file_content', { file_path: file.path })
        .then(response => {
          console.log("get file content", file.path)
          this.selectedMutOutputContent = response.data.content;
          console.log(response.data.content)
          this.mutOutputLoading = false
        })
        .catch(error => {
          console.error('Error fetching file content:', error);
        });
    },

    submitRunCaseConfigForm(){
      this.running = true
      this.$axios.post('/api/web_run', this.runCaseConfigForm)
        .then(response => {
          this.mutOutputFilesForRun = response.data.mutOutputFilesForRun;
          this.runStat = response.data.runStat
          console.log(response)
          this.running = false
        })
        .catch(error => {
          console.error('Error fetching file content:', error);
        });
    },

    addRunCase() {
      this.runCaseConfigForm.push(
        {
          file: '',
          argv: '',
        }
      )
    },

    delRunCase(index) {
      this.runCaseConfigForm.splice(index, 1);
    },

    resetRunCase(){
      // reset run case config form
      this.runCaseConfigForm = [].concat(this.defaultRunCaseConfigForm);
    },

    submitForm(formName) {
        this.$refs[formName].validate((valid) => {
          if (valid) {
            alert('submit!');
          } else {
            console.log('error submit!!');
            return false;
          }
        });
      },
    resetForm(formName) {
      this.$refs[formName].resetFields();
    },
    removeDomain(item) {
      var index = this.dynamicValidateForm.domains.indexOf(item)
      if (index !== -1) {
        this.dynamicValidateForm.domains.splice(index, 1)
      }
    },
    addDomain() {
      this.dynamicValidateForm.domains.push({
        value: '',
        key: Date.now()
      });
    },


    async getFileContent() {
      try {
        // const response = await this.$axios.get('/api/get_file_content');
        // this.fileContent = response.data.content;
        
        await this.$axios
          .get('/api/get_file_content')
          .then(response => (this.fileContent = response.data.content))
          .catch(function (error) { // 请求失败处理
            console.log(error);
          });

      } catch (error) {
        console.error('Error fetching file content:', error);
      }
    },

    // getFileContent(file_path) {
    //   this.$axios.post('/api/get_file_content', { file_path: filePath })
    //     .then(response => {
    //       this.fileContent = response.data.content;
    //     })
    //     .catch(error => {
    //       console.error('Error fetching file content:', error);
    //     });
    // },

    async handleFileClick(data) {
      console.log(data.label)
      console.log(data.path)
      this.sourceFileLoading = true
      this.$axios.post('/api/get_file_content', { file_path: data.path })
        .then(response => {
          this.cur_file_content = response.data.content;
          console.log(response.data.content)
          this.sourceFileLoading = false

        })
        .catch(error => {
          console.error('Error fetching file content:', error);
        });
    },

    selectSubject(command) {
      if (command === "demo") {
        this.getDemoSrc()
      }
    },

    async getDemoSrc() {
      try {
        console.log("get demo src\n")
        await this.$axios
          .get('/api/get_demo_src')
          .then(response => (this.foldersData = response.data.data))
          .catch(function (error) { // 请求失败处理
            console.log(error);
          });

      } catch (error) {
        console.error('Error getting demo src:', error);
      }
    }
  },

  
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

h1 {
  font-size: 2em;
  margin-bottom: 20px;
}

p {
  font-size: 1.2em;
}
</style>
