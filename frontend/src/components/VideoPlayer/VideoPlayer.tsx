import {
  useRef,
  useEffect,
  useCallback,
  useState,
  forwardRef,
  useImperativeHandle,
} from "react";
import type { VideoInfo } from "../../types";
import styles from "./VideoPlayer.module.css";

interface Props {
  videoUrl: string | null;
  videoInfo: VideoInfo | null;
  onCanvasReady?: (canvas: HTMLCanvasElement) => void;
  onFrameChange?: (frame: number) => void;
}

export interface VideoPlayerHandle {
  getCurrentFrame: () => number;
  seekToFrame: (frame: number) => void;
  getCanvasSize: () => { width: number; height: number };
}

const SPEEDS = [0.5, 1, 2, 4];

export const VideoPlayer = forwardRef<VideoPlayerHandle, Props>(
  ({ videoUrl, videoInfo, onCanvasReady, onFrameChange }, ref) => {
    const videoRef = useRef<HTMLVideoElement>(null);
    const canvasRef = useRef<HTMLCanvasElement>(null);
    const containerRef = useRef<HTMLDivElement>(null);
    const rafRef = useRef<number>(0);

    const [playing, setPlaying] = useState(false);
    const [currentTime, setCurrentTime] = useState(0);
    const [speed, setSpeed] = useState(1);

    const fps = videoInfo?.fps ?? 25;
    const duration = videoInfo?.duration ?? 0;
    const totalFrames = videoInfo?.total_frames ?? 0;
    const currentFrame = Math.round(currentTime * fps);

    // canvas 크기를 영상 비율에 맞추기 (사용 가능 높이 초과 방지)
    const updateCanvasSize = useCallback(() => {
      const container = containerRef.current;
      const canvas = canvasRef.current;
      if (!container || !canvas || !videoInfo) return;

      const aspectRatio = videoInfo.height / videoInfo.width;
      const maxWidth = container.clientWidth;

      // .video-area 요소를 찾아 flex 레이아웃이 결정한 높이를 사용 (순환 참조 방지)
      const videoArea = container.closest('.video-area');
      const availableHeight = videoArea
        ? videoArea.clientHeight - 130  // 컨트롤 + padding
        : window.innerHeight * 0.6;

      let canvasWidth = maxWidth;
      let canvasHeight = Math.round(maxWidth * aspectRatio);

      // 높이 초과 시 높이 기준으로 역산
      if (canvasHeight > availableHeight && availableHeight > 0) {
        canvasHeight = Math.round(availableHeight);
        canvasWidth = Math.round(canvasHeight / aspectRatio);
      }

      canvas.width = canvasWidth;
      canvas.height = canvasHeight;
      canvas.style.width = `${canvasWidth}px`;
      canvas.style.height = `${canvasHeight}px`;

      onCanvasReady?.(canvas);
    }, [videoInfo, onCanvasReady]);

    // 최신 함수를 ref로 유지 (useEffect deps 오염 방지)
    const lastTimeRef = useRef(-1);
    const updateCanvasSizeRef = useRef(updateCanvasSize);
    updateCanvasSizeRef.current = updateCanvasSize;

    const renderFrame = useCallback(() => {
      const video = videoRef.current;
      const canvas = canvasRef.current;
      if (!video || !canvas) return;

      const ctx = canvas.getContext("2d");
      if (!ctx) return;

      if (video.readyState >= video.HAVE_CURRENT_DATA) {
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
      }

      const t = video.currentTime;
      if (t !== lastTimeRef.current) {
        lastTimeRef.current = t;
        setCurrentTime(t);
        onFrameChange?.(Math.round(t * fps));
      }

      if (!video.paused) {
        rafRef.current = requestAnimationFrame(renderFrame);
      }
    }, [fps, onFrameChange]);

    const renderFrameRef = useRef(renderFrame);
    renderFrameRef.current = renderFrame;

    // 영상 로드 시 렌더 루프 시작 (videoUrl만 의존)
    useEffect(() => {
      const video = videoRef.current;
      if (!video || !videoUrl) return;

      video.src = videoUrl;
      video.load();

      const handleLoaded = () => {
        // videoInfo 도착 전에도 1회 시도 (이미 있으면 성공)
        updateCanvasSizeRef.current();
        renderFrameRef.current();
      };

      video.addEventListener("loadeddata", handleLoaded);
      return () => {
        video.removeEventListener("loadeddata", handleLoaded);
        cancelAnimationFrame(rafRef.current);
      };
    }, [videoUrl]);

    // videoInfo 도착 후 canvas 크기 재설정 + 첫 프레임 렌더
    useEffect(() => {
      if (!videoInfo) return;
      updateCanvasSizeRef.current();
      renderFrameRef.current();
    }, [videoInfo]);

    // 창 리사이즈 시 canvas 크기 재조정
    useEffect(() => {
      const handleResize = () => updateCanvasSizeRef.current();
      window.addEventListener("resize", handleResize);
      return () => window.removeEventListener("resize", handleResize);
    }, []);

    // 일시정지 상태에서 canvas를 한 번 다시 그림
    const renderOnce = useCallback(() => {
      cancelAnimationFrame(rafRef.current);
      rafRef.current = requestAnimationFrame(renderFrame);
    }, [renderFrame]);

    useImperativeHandle(ref, () => ({
      getCurrentFrame: () => Math.round((videoRef.current?.currentTime ?? 0) * fps),
      seekToFrame: (frame: number) => {
        if (videoRef.current) {
          videoRef.current.currentTime = frame / fps;
          renderOnce();
        }
      },
      getCanvasSize: () => ({
        width: canvasRef.current?.width ?? 0,
        height: canvasRef.current?.height ?? 0,
      }),
    }));

    // 재생/일시정지
    const togglePlay = useCallback(() => {
      const video = videoRef.current;
      if (!video) return;
      if (video.paused) {
        video.play();
        setPlaying(true);
        rafRef.current = requestAnimationFrame(renderFrame);
      } else {
        video.pause();
        setPlaying(false);
      }
    }, [renderFrame]);

    // 프레임 이동
    const stepFrame = useCallback(
      (delta: number) => {
        const video = videoRef.current;
        if (!video) return;
        video.pause();
        setPlaying(false);
        video.currentTime = Math.max(0, Math.min(video.currentTime + delta / fps, duration));
        renderOnce();
      },
      [fps, duration, renderOnce]
    );

    // 5초 점프
    const jump = useCallback(
      (seconds: number) => {
        const video = videoRef.current;
        if (!video) return;
        video.currentTime = Math.max(0, Math.min(video.currentTime + seconds, duration));
        renderOnce();
      },
      [duration, renderOnce]
    );

    // 시간 슬라이더
    const handleSlider = useCallback(
      (e: React.ChangeEvent<HTMLInputElement>) => {
        const video = videoRef.current;
        if (!video) return;
        video.currentTime = parseFloat(e.target.value);
        renderOnce();
      },
      [renderOnce]
    );

    // 재생 속도
    const changeSpeed = useCallback((s: number) => {
      const video = videoRef.current;
      if (!video) return;
      video.playbackRate = s;
      setSpeed(s);
    }, []);

    // 키보드 단축키: ←/→
    useEffect(() => {
      const handleKey = (e: KeyboardEvent) => {
        if (e.key === "ArrowLeft") {
          e.preventDefault();
          stepFrame(-1);
        } else if (e.key === "ArrowRight") {
          e.preventDefault();
          stepFrame(1);
        }
      };
      window.addEventListener("keydown", handleKey);
      return () => window.removeEventListener("keydown", handleKey);
    }, [stepFrame]);

    const formatTime = (t: number) => {
      const m = Math.floor(t / 60);
      const s = (t % 60).toFixed(1);
      return `${m}:${s.padStart(4, "0")}`;
    };

    return (
      <div className={styles.container}>
        <div ref={containerRef} className={styles.canvasContainer}>
          <canvas ref={canvasRef} className={styles.videoCanvas} />
          {/* fabric-canvas는 ZoneEditor가 이 위에 겹침 */}
          <video ref={videoRef} muted playsInline style={{ display: "none" }} />
        </div>

        <div className={styles.controls}>
          <div className={styles.buttons}>
            <button onClick={() => jump(-5)} title="5초 뒤로">⏪</button>
            <button onClick={() => stepFrame(-1)} title="1프레임 뒤로">◀</button>
            <button onClick={togglePlay} title={playing ? "일시정지" : "재생"}>
              {playing ? "⏸" : "▶"}
            </button>
            <button onClick={() => stepFrame(1)} title="1프레임 앞으로">▶</button>
            <button onClick={() => jump(5)} title="5초 앞으로">⏩</button>
          </div>

          <div className={styles.speedButtons}>
            {SPEEDS.map((s) => (
              <button
                key={s}
                onClick={() => changeSpeed(s)}
                className={speed === s ? styles.activeSpeed : ""}
              >
                {s}x
              </button>
            ))}
          </div>

          <div className={styles.timeInfo}>
            <span>{formatTime(currentTime)}</span>
            <span> / {formatTime(duration)}</span>
            <span className={styles.frameInfo}>
              프레임: {currentFrame} / {totalFrames}
            </span>
          </div>

          <input
            type="range"
            min={0}
            max={duration || 1}
            step={0.01}
            value={currentTime}
            onChange={handleSlider}
            className={styles.slider}
          />
        </div>
      </div>
    );
  }
);

VideoPlayer.displayName = "VideoPlayer";
