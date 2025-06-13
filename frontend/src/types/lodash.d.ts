/* eslint-disable @typescript-eslint/no-explicit-any */

declare module 'lodash' {
  export function debounce<T extends (...args: any[]) => any>(
    func: T,
    wait?: number,
    options?: {
      leading?: boolean;
      maxWait?: number;
      trailing?: boolean;
    }
  ): T;
}

declare module 'lodash/debounce' {
  import { debounce } from 'lodash';
  export = debounce;
}