/* eslint-disable @next/next/no-img-element */
import Bar from "@/components/Bar";
import getStream from "@/utils/camera";
import { getEmotion } from "@/utils/socket/getEmotion";
import { Slider } from "@mui/material";
import { useRouter } from "next/router"
import { useCallback, useEffect, useId, useRef, useState } from "react"
import NavigateNextIcon from '@mui/icons-material/NavigateNext';
import { throttle } from "lodash";
import { Pie1Chart, Pie1DataProps, Pie2Chart, RadarChart } from "@/components/Chart";
import { updatePie1Data } from "@/utils/method/updatePie1Data";
import CircularProgress from '@mui/material/CircularProgress';

export default function Report() {

  const router = useRouter();
  
  const {id} = router.query;
}