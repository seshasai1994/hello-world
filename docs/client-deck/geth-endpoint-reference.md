# Geth Endpoint Reference → Dashboard Mapping

Complete catalog of every Geth interface, mapped to the trader suite (T),
compliance/security suite (C), and ops/platform health (O) dashboards.
Includes "Why Geth Alone Is Not Enough" with corrected 2026 storage figures.

---

## 1. `eth_` namespace (core)

| Endpoint | Purpose | Feeds |
|---|---|---|
| `eth_blockNumber` | Current head block | T/C/O freshness badge, sync lag |
| `eth_chainId` | Chain identifier | O sanity checks |
| `eth_syncing` | Sync progress or false | O node health |
| `eth_getBlockByNumber` | Full block (txs, gas, baseFee, timestamp) | T tape/gas; C incident timelines |
| `eth_getBlockByHash` | Block by hash | T/C reorg handling |
| `eth_getBlockReceipts` | All receipts for a block in one call | T/C most efficient ingestion endpoint |
| `eth_getBlockTransactionCountByNumber` | Tx count per block | T congestion |
| `eth_getBlockTransactionCountByHash` | Same by hash | T congestion |
| `eth_getUncleByBlockHashAndIndex` | Uncle data | O (post-merge: empty) |
| `eth_getUncleByBlockNumberAndIndex` | Uncle data | O |
| `eth_getUncleCountByBlockHash` | Uncle count | O |
| `eth_getUncleCountByBlockNumber` | Uncle count | O |
| `eth_getTransactionByHash` | Tx details | T execution desk; C evidence |
| `eth_getTransactionByBlockNumberAndIndex` | Tx by block position | T MEV-neighbor analysis |
| `eth_getTransactionByBlockHashAndIndex` | Same by hash | T |
| `eth_getTransactionReceipt` | Status, gas used, logs | T success/fail/slippage; C proof of payment |
| `eth_getTransactionCount` | Account nonce | T stuck/replaced tx detection |
| `eth_getRawTransactionByHash` | Raw RLP tx | C forensic export |
| `eth_getRawTransactionByBlockHashAndIndex` | Raw tx | C |
| `eth_getRawTransactionByBlockNumberAndIndex` | Raw tx | C |
| `eth_getBalance` | ETH balance at any block | T portfolio; C treasury snapshots |
| `eth_getCode` | Contract bytecode | C contract/EOA check, bytecode families |
| `eth_getStorageAt` | Raw storage slot | C proxy/owner slot forensics |
| `eth_getProof` | Merkle proof | C cryptographic evidence (limited history on path-archive) |
| `eth_getLogs` | Event logs by address/topic/range | T/C backbone: transfers, swaps, approvals, LP, admin events |
| `eth_newFilter` | Server-side log filter | T live watchers |
| `eth_newBlockFilter` | New-block filter | T tape |
| `eth_newPendingTransactionFilter` | Pending tx filter | T mempool |
| `eth_getFilterChanges` | Poll filter deltas | T |
| `eth_getFilterLogs` | Full filter results | T |
| `eth_uninstallFilter` | Cleanup | O |
| `eth_call` | Read contract state | T token metadata, portfolio; C honeypot sell-probe |
| `eth_estimateGas` | Gas estimation | T execution planning |
| `eth_createAccessList` | Access list + gas | T execution optimization |
| `eth_simulateV1` | Multi-call/block simulation (Geth >= 1.14) | T pre-trade sim; C approval impact |
| `eth_feeHistory` | Base fee + tip percentiles history | T gas heatmap, overpay analytics |
| `eth_gasPrice` | Current gas price | T top strip |
| `eth_maxPriorityFeePerGas` | Suggested tip | T execution desk |
| `eth_blobBaseFee` | Blob base fee (EIP-4844) | T L2 posting panel |
| `eth_sendRawTransaction` | Broadcast signed tx | not in v1 (no execution) |
| `eth_sendTransaction` | Node-signed send | never expose |
| `eth_sign` / `eth_signTransaction` | Node-side signing | never expose |
| `eth_fillTransaction` | Fill tx defaults (Geth ext.) | — |
| `eth_accounts` | Node accounts | empty in prod; unused |
| `eth_coinbase` | Coinbase address | deprecated |
| `eth_getHeaderByNumber` / `eth_getHeaderByHash` | Lightweight headers (Geth ext.) | O cheap sync monitor |
| `eth_pendingTransactions` | Node's pending txs | T mempool gauge |
| `eth_protocolVersion` | Protocol version | deprecated |
| `eth_mining` / `eth_hashrate` | PoW relics | dead post-merge |
| `eth_getWork` / `eth_submitWork` / `eth_submitHashrate` | PoW mining | removed |

## 2. WebSocket subscriptions (`eth_subscribe` / `eth_unsubscribe`)

| Subscription | Feeds |
|---|---|
| `newHeads` | T live tape trigger; O head-age alarm |
| `logs` (filtered) | T real-time swaps/transfers/LP; C treasury/approval alerts |
| `newPendingTransactions` | T mempool congestion, pre-inclusion watch |
| `syncing` | O sync state changes |

These four are the difference between a 1–3 s tape and a polling toy.

## 3. `debug_` namespace (internal transactions live here)

Critical subset — captures contract-to-contract ETH transfers that logs miss:

| Endpoint | Purpose | Feeds |
|---|---|---|
| `debug_traceTransaction` | Call tree of one tx (callTracer / prestateTracer) | T revert analysis; C internal fund-flow, incidents |
| `debug_traceBlockByNumber` | Trace every tx in block | T/C bulk internal-transfer indexing |
| `debug_traceBlockByHash` | Same by hash | T/C |
| `debug_traceBlock` | Trace RLP block | C |
| `debug_traceCall` | Trace hypothetical call | T honeypot sell-sim; C what-if evidence |
| `debug_traceChain` | Trace block range | C backfills |
| `debug_traceBadBlock` / `debug_getBadBlocks` | Rejected block forensics | O |
| `debug_standardTraceBlockToFile` / `debug_standardTraceBadBlockToFile` | Traces to disk | O offline analysis |
| `debug_getModifiedAccountsByNumber` | Accounts touched in block | C affected-party scans |
| `debug_getModifiedAccountsByHash` | Same by hash | C |
| `debug_getRawBlock` / `debug_getRawHeader` / `debug_getRawReceipts` / `debug_getRawTransaction` | Raw RLP | C evidence archival |
| `debug_dumpBlock` | State dump at block | C deep forensics (archive) |
| `debug_accountRange` | Iterate accounts at block | C state analytics (archive) |
| `debug_storageRangeAt` | Iterate contract storage | C proxy/ownership forensics |
| `debug_intermediateRoots` | State roots per tx | research |
| `debug_preimage` | Hash preimage | research |
| `debug_getAccessibleState` | Nearest available state | O archive coverage |
| `debug_dbGet` / `debug_dbAncient` / `debug_dbAncients` | Raw DB reads | O |
| `debug_chaindbCompact` / `debug_chaindbProperty` | DB maintenance | O |
| `debug_setHead` | Rewind chain head (dangerous) | ops only, never exposed |
| `debug_setTrieFlushInterval` | State flush tuning | O |
| `debug_freezeClient` | Test freezer | — |
| Profiling: `debug_cpuProfile`, `debug_startCPUProfile`, `debug_stopCPUProfile`, `debug_goTrace`, `debug_startGoTrace`, `debug_stopGoTrace`, `debug_blockProfile`, `debug_setBlockProfileRate`, `debug_writeBlockProfile`, `debug_mutexProfile`, `debug_setMutexProfileFraction`, `debug_writeMutexProfile`, `debug_memStats`, `debug_gcStats`, `debug_freeOSMemory`, `debug_setGCPercent`, `debug_writeMemProfile`, `debug_stacks`, `debug_verbosity`, `debug_vmodule`, `debug_backtraceAt`, `debug_printBlock` | Node performance profiling | O platform health only |

Security: never expose `debug_` publicly — compute-heavy DoS vector, and
`debug_setHead` can wreck node state. Private indexer node only.

## 4. `txpool_` namespace (own-node mempool)

| Endpoint | Feeds |
|---|---|
| `txpool_status` | T pending/queued counts, congestion gauge |
| `txpool_content` | T full pending bodies, pre-inclusion whale watch |
| `txpool_contentFrom` | T/C pending txs of watched address |
| `txpool_inspect` | T readable pool summary |

## 5. `net_` / `web3_`

| Endpoint | Feeds |
|---|---|
| `net_version` | O network ID |
| `net_listening` | O P2P health |
| `net_peerCount` | O peer gauge (alert < 5) |
| `web3_clientVersion` | O version tracking |
| `web3_sha3` | utility (do in app code) |

## 6. `admin_` (private ops only)

`admin_nodeInfo`, `admin_peers`, `admin_peerEvents`, `admin_addPeer`,
`admin_removePeer`, `admin_addTrustedPeer`, `admin_removeTrustedPeer`,
`admin_datadir`, `admin_exportChain`, `admin_importChain`,
`admin_startHTTP`, `admin_stopHTTP`, `admin_startWS`, `admin_stopWS`
— all O: peer management + RPC lifecycle. Never public.

## 7. Namespaces you will not use (completeness)

- **`engine_`** — `engine_newPayloadV1–V4`, `engine_forkchoiceUpdatedV1–V3`,
  `engine_getPayloadV1–V4`, `engine_getPayloadBodiesByHashV1/ByRangeV1`,
  `engine_exchangeCapabilities`. Authenticated port 8551, reserved for the
  consensus client. This is the "Geth cannot run alone" requirement in
  protocol form.
- **`personal_`** — deprecated/removed (`personal_newAccount`,
  `personal_unlockAccount`, `personal_sendTransaction`, `personal_sign`,
  `personal_ecRecover`, `personal_importRawKey`, etc.). Key management
  belongs in Clef/user wallets; no-custody scope never needs it.
- **`miner_`** — dead post-merge (`miner_start`, `miner_stop`,
  `miner_setEtherbase`, `miner_setExtra`, `miner_setGasPrice`, `miner_setGasLimit`).
- **`clique_`** — PoA testnets only (`clique_getSigners`, `clique_getSnapshot`,
  `clique_propose`, `clique_discard`, `clique_status`, ...).
- **`les_`** — light-client server, effectively abandoned.

## 8. Non-JSON-RPC interfaces

| Interface | Feeds |
|---|---|
| GraphQL (`--graphql`, EIP-1767 schema) | T/C batched queries, backfill scripts |
| Prometheus metrics (`--metrics`, :6060) | O node section of platform health |
| P2P/discovery (30303) | O connectivity |
| Auth RPC (8551, JWT) | consensus client only |

---

## 9. Why Geth alone is not enough (corrected figures, 2026)

1. **Consensus client required.** Post-merge, Geth cannot follow the chain
   alone; Lighthouse/Prysm drives it via the `engine_` API.
2. **Pruned vs archive.** Snap-synced full node: ~0.8–1.3 TB of data
   (2 TB drive advised). Legacy hash-based archive: 12–20+ TB.
   **Geth v1.16+ path-based archive: ~1.9–2.2 TB** — changed the economics;
   trade-off is limited historical `eth_getProof`.
3. **Internal transactions.** Plain ETH transfers between contracts emit no
   logs. Only `debug_trace*` (or Erigon `trace_`) reveals them. Fund-flow or
   whale products without trace indexing silently miss a large fraction of
   ETH movement — a compliance-suite dealbreaker.
4. **Erigon alternative.** Archive in ~2–3 TB; adds `trace_` namespace
   (`trace_block`, `trace_transaction`, `trace_filter`, `trace_call`,
   `trace_replayTransaction`). `trace_filter` — "all internal transfers
   touching address X in range" in one call — has no Geth equivalent and
   alone justifies running Erigon beside Geth if the compliance suite is the
   revenue center. Wants >= 32 GB RAM, 4 TB NVMe, and a consensus client
   (or embedded Caplin).
5. **Indexers.** The node answers "what's in block N", never "all activity
   of address A between X and Y". That is the PostgreSQL/ClickHouse
   pipeline (chosen), TrueBlocks (local address index), or The Graph
   (subgraphs).

## 10. Endpoint-to-dashboard summary

| Dashboard | Primary endpoints |
|---|---|
| Live Tape | `eth_subscribe(newHeads, logs)`, `eth_getBlockReceipts` |
| Token Cockpit | `eth_getLogs`, `eth_call`, `debug_traceCall` |
| Liquidity Events | `eth_getLogs` (Mint/Burn topics) |
| Whale/Flow Tape | `eth_getLogs` + `debug_traceBlockByNumber` |
| Execution Desk | `eth_getTransactionReceipt`, `eth_feeHistory`, `eth_getTransactionByBlockNumberAndIndex`, `debug_traceTransaction` |
| Portfolio | `eth_getBalance`, `eth_call` (balanceOf) |
| Gas Heatmap | `eth_feeHistory`, `eth_gasPrice`, `eth_blobBaseFee` |
| Exposure Screening (C) | indexed transfers + `debug_traceChain` + published lists |
| Approval Monitor (C) | `eth_getLogs` (Approval topics) |
| Treasury Board (C) | `eth_getBalance`, `eth_subscribe(logs)`, `txpool_contentFrom` |
| Incident Workspace (C) | `debug_traceTransaction`, `debug_getModifiedAccountsByNumber`, raw getters |
| Contract Forensics (C) | `eth_getCode`, `eth_getStorageAt`, `eth_getProof`, `debug_storageRangeAt` |
| Platform Health (O) | metrics endpoint, `eth_syncing`, `net_peerCount`, `txpool_status`, `admin_peers` |

Namespaces covered: `eth`, `debug`, `txpool`, `net`, `web3`, `admin`,
`engine`, `personal` (removed), `miner` (dead), `clique` (PoA), `les`
(abandoned), plus GraphQL and Prometheus metrics.
