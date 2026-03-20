import { useState } from "react";
import type { ZoneDefinition } from "../../types";
import { ZONE_BORDER_COLORS } from "../../types";
import styles from "./ZonePanel.module.css";

interface Props {
  zones: ZoneDefinition[];
  selectedZoneId: string | null;
  mode: "zone-edit" | "annotation";
  zoneConfigs: string[];
  selectedConfig: string;
  onSelectZone: (zoneId: string | null) => void;
  onAddZone: (name: string, type: "danger" | "warning" | "entry") => void;
  onDeleteZone: (zoneId: string) => void;
  onSaveConfig: (configName: string) => void;
  onLoadConfig: (configName: string) => void;
}

export function ZonePanel({
  zones,
  selectedZoneId,
  mode,
  zoneConfigs,
  selectedConfig,
  onSelectZone,
  onAddZone,
  onDeleteZone,
  onSaveConfig,
  onLoadConfig,
}: Props) {
  const [showAddDialog, setShowAddDialog] = useState(false);
  const [newName, setNewName] = useState("");
  const [newType, setNewType] = useState<"danger" | "warning" | "entry">("danger");
  const [saveName, setSaveName] = useState(selectedConfig || "zones.yaml");

  const handleAdd = () => {
    if (!newName.trim()) return;
    onAddZone(newName.trim(), newType);
    setNewName("");
    setNewType("danger");
    setShowAddDialog(false);
  };

  return (
    <div className={styles.panel}>
      <h3 className={styles.title}>Zone 목록</h3>

      {/* 설정 파일 로드/저장 */}
      <div className={styles.configSection}>
        <select
          value={selectedConfig}
          onChange={(e) => onLoadConfig(e.target.value)}
          className={styles.configSelect}
        >
          <option value="">설정 선택...</option>
          {zoneConfigs.map((c) => (
            <option key={c} value={c}>{c}</option>
          ))}
        </select>
        {mode === "zone-edit" && (
          <div className={styles.saveRow}>
            <input
              type="text"
              value={saveName}
              onChange={(e) => setSaveName(e.target.value)}
              className={styles.saveInput}
              placeholder="파일명.yaml"
            />
            <button onClick={() => onSaveConfig(saveName)} className={styles.btn}>
              저장
            </button>
          </div>
        )}
      </div>

      {/* Zone 목록 */}
      <div className={styles.list}>
        {zones.map((z) => (
          <div
            key={z.zone_id}
            className={`${styles.item} ${z.zone_id === selectedZoneId ? styles.selected : ""}`}
            onClick={() => onSelectZone(z.zone_id === selectedZoneId ? null : z.zone_id)}
          >
            <span
              className={styles.dot}
              style={{ background: ZONE_BORDER_COLORS[z.zone_type] }}
            />
            <span className={styles.name}>{z.zone_name}</span>
            <span className={styles.type}>{z.zone_type}</span>
          </div>
        ))}
        {zones.length === 0 && (
          <p className={styles.empty}>zone 없음</p>
        )}
      </div>

      {/* 추가/삭제 버튼 */}
      {mode === "zone-edit" && (
        <div className={styles.actions}>
          <button onClick={() => setShowAddDialog(true)} className={styles.btn}>
            + 추가
          </button>
          <button
            onClick={() => selectedZoneId && onDeleteZone(selectedZoneId)}
            disabled={!selectedZoneId}
            className={styles.btnDanger}
          >
            - 삭제
          </button>
        </div>
      )}

      {/* 추가 다이얼로그 */}
      {showAddDialog && (
        <div className={styles.dialog}>
          <h4>새 Zone</h4>
          <input
            type="text"
            value={newName}
            onChange={(e) => setNewName(e.target.value)}
            placeholder="이름"
            className={styles.input}
            autoFocus
          />
          <select
            value={newType}
            onChange={(e) => setNewType(e.target.value as any)}
            className={styles.input}
          >
            <option value="danger">danger</option>
            <option value="warning">warning</option>
            <option value="entry">entry</option>
          </select>
          <div className={styles.dialogActions}>
            <button onClick={handleAdd} className={styles.btn}>확인</button>
            <button onClick={() => setShowAddDialog(false)} className={styles.btnSecondary}>
              취소
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
